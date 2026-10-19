"""Verify the bytes a publisher will upload; never install or submit a plugin."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import jsonschema

HERE = Path(__file__).resolve().parent
SCHEMAS = Path(os.environ.get('PLUGIN_SCHEMA_DIR', HERE / 'schemas'))


class PublicationPackageTests(unittest.TestCase):
    def test_each_host_receives_its_own_embedded_configuration(self):
        schema = json.loads((SCHEMAS / 'mcp.schema.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory() as directory:
            archives = {}
            for target in ('portable', 'openai'):
                output = Path(directory) / f'{target}.zip'
                subprocess.run([sys.executable, str(HERE / 'build_package.py'),
                    '--target', target, '--output', str(output), '--schema-dir', str(SCHEMAS)],
                    check=True, capture_output=True, text=True)
                with zipfile.ZipFile(output) as archive:
                    archives[target] = {name: archive.read(name) for name in archive.namelist()}
            portable = json.loads(archives['portable']['mcp.json'])
            openai = json.loads(archives['openai']['mcp.json'])
            jsonschema.Draft202012Validator(schema).validate(portable)
            self.assertNotIn('extensions', portable['mcpServers']['abigail'])
            self.assertEqual(openai['mcpServers']['abigail']['extensions']['com.openai']['auth'],
                             {'type': 'oauth', 'client': {'mode': 'dcr'}})
            # The unchanged external portable schema rejects vendor server extensions.
            # Do not weaken it or falsely label the OpenAI artifact portable-valid.
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.Draft202012Validator(schema).validate(openai)
            self.assertEqual(set(archives['portable']), set(archives['openai']))
            self.assertEqual(len(archives['openai']), 7)
            self.assertEqual(hashlib.sha256(archives['openai']['LICENSE.md']).hexdigest(),
                '761bcbdbcd3f3b09b9736041c9a1bc887c1a6b40e871a98ae0683bb7d9a327f6')
            for name in archives['portable']:
                if name != 'mcp.json':
                    self.assertEqual(archives['portable'][name], archives['openai'][name])
            self.assertNotIn('openai-auth-settings.json', archives['openai'])

    def test_openai_contract_rejects_missing_auth_secrets_and_unknown_fields(self):
        from build_package import validate_openai_mcp
        valid = {'$schema': 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json',
                 'mcpServers': {'abigail': {'type': 'streamable-http',
                     'url': 'https://mcp.abigail.app/mcp',
                     'extensions': {'com.openai': {'auth': {
                         'type': 'oauth', 'client': {'mode': 'dcr'}}}}}}}
        validate_openai_mcp(valid)
        for mutation in ('missing', 'secret', 'headers'):
            value = json.loads(json.dumps(valid))
            server = value['mcpServers']['abigail']
            if mutation == 'missing':
                del server['extensions']
            elif mutation == 'secret':
                server['extensions']['com.openai']['auth']['clientSecret'] = 'synthetic-test'
            else:
                server['headers'] = {'Authorization': 'synthetic-test'}
            with self.assertRaises(jsonschema.ValidationError):
                validate_openai_mcp(value)


if __name__ == '__main__':
    unittest.main()
