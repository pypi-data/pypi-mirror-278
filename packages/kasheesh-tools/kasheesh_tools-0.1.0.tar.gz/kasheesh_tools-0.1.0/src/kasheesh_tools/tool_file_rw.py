"""This is the tool used to read/write parquet/csv files from/to s3/local.
"""


import os
import shutil

import pandas as pd
import s3fs
from pyarrow import parquet as pq, Table
import uuid

from kasheesh_tools.tool_logger import get_my_logger

class FileHandler:
    def __init__(self, name="FileHdlr") -> None:
        self.logger = get_my_logger(name=name, level="INFO")

    def write_parquet(self, df, root_path, partition_cols=None, use_threads=6, overwrite=False,
                      date_of_job: str = "date", job_name: str = "job", keep_unique=True):
        """write parquet file from s3 or local

        Args:
            df (pd.DataFrame): dataframe to write
            root_path (str): root path to write
            partition_cols (list, optional): columns to partition, ORDERED AS SPECIFIED. Defaults to None.
            use_threads (int/bool, optional): threads count. Default cpu_count(). Forced Default to 6.
            overwrite (bool, optional): overwrite existing file. Defaults to False.
            date_of_job (str, optional): date of job (YYYYMMDD). Defaults to "date".
            job_name (str, optional): job name. Defaults to "job".
        """
        if 'datadate' not in df.columns:
            df['datadate'] = pd.Timestamp.now().date()
            self.logger.info(f"Added datadate column to dataframe.")
        self.logger.info(f"Writing {df.shape} dataframe to {root_path}")
        overwrite_behavior = None  # default: removing only the files with the same name.
        if overwrite:
            overwrite_behavior = 'delete_matching'  # removing the whole partition, all files in it.
        if keep_unique:
            uuid_str = uuid.uuid4().hex
        else:
            uuid_str = ""
        if "s3://" in root_path:
            fs = s3fs.S3FileSystem()
            pq.write_to_dataset(
                Table.from_pandas(df),
                root_path,
                partition_cols=partition_cols,
                filesystem=fs,
                use_dictionary=True,
                compression="snappy",
                existing_data_behavior=overwrite_behavior,
                basename_template = "{job_name}-{date_of_job}-{uuid}-{{i}}.parquet".format(date_of_job=date_of_job, 
                                                                                           job_name=job_name,
                                                                                           uuid=uuid_str)
            )
        else:
            # df.to_parquet(root_path, partition_cols=partition_cols, use_threads=use_threads)
            pq.write_to_dataset(
                Table.from_pandas(df),
                root_path,
                partition_cols=partition_cols,
                use_dictionary=True,
                compression="snappy",
                existing_data_behavior=overwrite_behavior,
                basename_template = "{job_name}-{date_of_job}-{{i}}-{uuid}.parquet".format(date_of_job=date_of_job, 
                                                                                           job_name=job_name,
                                                                                           uuid=uuid_str)
            )
            
        self.logger.info(f"Writing finished.")
        return None
    

    def read_parquet(self, root_path, filters=None, use_threads=6):
        """read parquet file from s3 or local

        Args:
            root_path (str): root path to read from
            filters (list, optional): Specify AND/OR conditions here. Defaults to None.
                    #readout_partial = FH.read_parquet(root_path=root_path, 
                        filters=[[("a", "=", 1)], [("a", "=", 3)]])  # This is OR condition
                    # readout_partial = FH.read_parquet(root_path=root_path, 
                        filters=[[("a", "=", 1), ("a", "=", 3)]])  # This is AND condition
            use_threads (int/bool, optional): threads count, Default cpu_count(). Forced Default to 6.

        Returns:
            df: pd.DataFrame
        """
        self.logger.info(f"Reading from {root_path}")
        if "s3://" in root_path:
            fs = s3fs.S3FileSystem()
            df = pq.ParquetDataset(root_path.replace("s3://", ""), filters=filters, filesystem=fs).read_pandas(use_threads=use_threads).to_pandas()
        else:
            df = pd.read_parquet(root_path, 
                                 filters=filters, use_threads=use_threads)
        self.logger.info(f"Reading finished. Data shape {df.shape}")
        return df
    
    def read_csv(self, file_path, use_env_creds=False):
        """read csv file from s3 or local

        Args:
            file_path (str): file path to read csv from

        Returns:
            df: pd.DataFrame
        """
        self.logger.info(f"Reading from {file_path}")
        if "s3://" in file_path:
            if use_env_creds and "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
                fs = s3fs.S3FileSystem(key=os.environ['AWS_ACCESS_KEY_ID'], 
                                       secret=os.environ['AWS_SECRET_ACCESS_KEY'])
            else:
                fs = s3fs.S3FileSystem()
            df = pd.read_csv(fs.open(file_path))
        else:
            df = pd.read_csv(file_path)
        self.logger.info(f"Reading finished. Data shape {df.shape}")
        return df
    
    def write_csv(self, df, file_path, use_env_creds=False, mode='w', index=False):
        """write csv file to s3 or local

        Args:
            df (pd.DataFrame): dataframe to write
            file_path (str): file path to write csv to
        """
        self.logger.info(f"Writing {df.shape} dataframe to {file_path}")
        if "s3://" in file_path:
            if use_env_creds and "AWS_ACCESS_KEY_ID" in os.environ and "AWS_SECRET_ACCESS_KEY" in os.environ:
                fs = s3fs.S3FileSystem(key=os.environ['AWS_ACCESS_KEY_ID'], 
                                       secret=os.environ['AWS_SECRET_ACCESS_KEY'])
            else:
                fs = s3fs.S3FileSystem()
            with fs.open(file_path, mode=mode) as f:
                df.to_csv(f, index=index)
        else:
            df.to_csv(file_path, mode=mode, index=index)
        self.logger.info(f"Writing finished.")
        return None


