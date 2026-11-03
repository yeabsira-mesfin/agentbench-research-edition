import unittest
import os
from unittest.mock import patch
from research.runner import compare, evaluate, task_spec, materialize
from tempfile import TemporaryDirectory
from pathlib import Path

class RunnerTests(unittest.TestCase):
    @unittest.skipUnless(os.getenv('RUN_TRUSTED_FIXTURES')=='1','trusted fixture execution requires explicit opt-in')
    def test_references_pass_and_faults_are_detected(self):
        data=compare()
        self.assertEqual(len(data['runs']),9)
        for r in data['runs']:
            if r['candidate_id']=='reference': self.assertTrue(r['release_ready'],r)
            elif r['candidate_id']=='faulty':
                self.assertEqual(r['groups']['visible']['status'],'pass')
                self.assertIn('security_failure',r['failure_categories'])
            else: self.assertIn('regression_failure',r['failure_categories'])
    def test_reject_arbitrary_inputs(self):
        for value in ('../bad','/etc/passwd','unknown'):
            with self.assertRaises(ValueError): task_spec(value)
            with self.assertRaises(ValueError): evaluate('SEC-411',value)
        with self.assertRaises(ValueError): compare(repeats=11)
    def test_hash_mismatch_prevents_execution(self):
        with patch('research.runner.digest',return_value='tampered'):
            with self.assertRaisesRegex(ValueError,'hash mismatch'): task_spec('SEC-411')
    def test_infrastructure_failure_is_distinct(self):
        fake={'status':'infrastructure_failure','tests':[],'exit_code':3}
        with patch('research.runner.run_group',return_value=fake):
            report=evaluate('SEC-411','reference')
            self.assertEqual(report['failure_categories'],['infrastructure_failure'])
            self.assertFalse(report['release_ready'])
    def test_patch_is_single_allowlisted_replacement(self):
        with TemporaryDirectory() as t:
            materialize('SEC-411','reference',Path(t))
            self.assertEqual({p.name for p in Path(t).iterdir()},{'solution.py','checks.py','child.py'})
    @unittest.skipUnless(os.getenv('RUN_TRUSTED_FIXTURES')=='1','trusted fixture execution requires explicit opt-in')
    def test_repeat_keeps_same_input_hash(self):
        data=compare(('SEC-411',),('reference',),2)
        self.assertEqual(data['runs'][0]['candidate_sha256'],data['runs'][1]['candidate_sha256'])

if __name__=='__main__': unittest.main()
