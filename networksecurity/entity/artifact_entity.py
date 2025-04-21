from dataclasses import dataclass
#we want to get the o/p of train and test file so that we use this class
@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str