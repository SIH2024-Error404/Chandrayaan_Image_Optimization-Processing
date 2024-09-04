import unittest
import os
import shutil
from src.psr_mapping import map_psr_and_save

class TestPSRMapping(unittest.TestCase):
    
    def setUp(self):
        self.image_path = 'data/raw/moon2.png'
        self.lunar_map_path = 'data/raw/lunar_map.png'
        self.export_dir = 'data/export'

    def test_map_psr_and_save_with_export(self):
        # Perform PSR mapping and export
        result_path = map_psr_and_save(self.image_path, self.lunar_map_path, self.export_dir)
        
        # Verify that the result is saved
        self.assertTrue(os.path.exists(result_path))
        
        # Verify that the PSR map is exported
        psr_map_export_path = os.path.join(self.export_dir, 'psr_mapped.png')
        self.assertTrue(os.path.exists(psr_map_export_path))
        
        # Verify that metadata is exported
        export_metadata_path = os.path.join(self.export_dir, 'metadata.json')
        self.assertTrue(os.path.exists(export_metadata_path))

    def tearDown(self):
        # Clean up after test
        if os.path.exists(self.export_dir):
            shutil.rmtree(self.export_dir)

if __name__ == '__main__':
    unittest.main()
