import logging
import os
import re
import boto3
from nwae.math.utils.Env import Env
from nwae.math.utils.Logging import Logging


class AwsS3Utils:

    def __init__(
            self,
            bucket_name,
            aws_access_id = None,
            aws_access_key = None,
            aws_region = None,
            logger = None,
    ):
        self.bucket_name = bucket_name
        self.aws_access_id = os.environ["AWS_ACCESS_ID"] if aws_access_id is None else aws_access_id
        self.aws_access_key = os.environ["AWS_ACCESS_KEY"] if aws_access_key is None else aws_access_key
        self.aws_region = os.environ["AWS_DEFAULT_REGION"] if aws_region is None else aws_region
        self.logger = logger if logger is not None else logging.getLogger()

        self.logger.info('AWS s3 bucket name "' + str(self.bucket_name))
        return

    def get_boto3_session(self):
        ssn = boto3.Session(
            aws_access_key_id = self.aws_access_id,
            aws_secret_access_key = self.aws_access_key,
            region_name = self.aws_region,
        )
        log_id = '*'*(len(self.aws_access_id)-5) + str(self.aws_access_id)[-5:]
        log_key = '*'*(len(self.aws_access_key)-5) + str(self.aws_access_key)[-5:]
        self.logger.info(
            'boto3 session created with AWS access key id "' + str(log_id)
            + '" & key "' + str(log_key) + '", region "' + str(self.aws_region) + '"'
        )
        return ssn

    def list_s3_objects(
            self,
            folder_prefix = None,
            encoding = None,
    ):
        session = self.get_boto3_session()
        s3 = session.client(service_name="s3")
        self.logger.info('Trying to list objects from bucket "' + str(self.bucket_name) + '"')
        if folder_prefix is None:
            result = s3.list_objects(
                Bucket = self.bucket_name,
            )
        else:
            result = s3.list_objects(
                Bucket = self.bucket_name,
                Prefix = folder_prefix,
            )

        self.logger.info('Retrieved result from bucket "' + str(self.bucket_name) + '": ' + str(result))
        objects = []
        for o in result.get('Contents', []):
            objects.append({
                'Key': o['Key'],
                'Size': o['Size'],
                'LastModified': o['LastModified'],
            })
        # for o in result.get('Contents'):
        #     data = s3.get_object(Bucket=self.bucket_name, Key=o.get('Key'))
        #     contents = data['Body'].read()
        #     if encoding is not None:
        #         # Binary file will fail to decode 'utf-8'
        #         contents_decoded = contents.decode("utf-8")
        #     else:
        #         contents_decoded = contents
        self.logger.info(
            'Total objects from bucket "' + str(self.bucket_name)
            + '", folder prefix "' + str(folder_prefix) + '" = ' + str(len(objects)) + '.'
        )
        return objects

    def read_s3_file(
            self,
            key,
            to_local_file,
    ):
        session = self.get_boto3_session()
        s3_client = session.client(service_name="s3")

        self.logger.info(
            'Download from bucket "' + str(self.bucket_name) + '" key "' + str(key)
            + '" to local file "' + str(to_local_file) + '"'
        )
        with open(to_local_file, 'wb') as data:
            s3_client.download_fileobj(self.bucket_name, key, data)

        # f = BytesIO()
        # s3_client.download_fileobj(self.bucket_name, key, f)
        self.logger.info(
            'DONE Download from bucket "' + str(self.bucket_name) + '" key "' + str(key)
            + '" to local file "' + str(to_local_file) + '"'
        )

        return to_local_file

    def upload_file(
            self,
            filepath,
            key,
    ):
        session = self.get_boto3_session()
        client = session.resource(service_name="s3")
        self.logger.info(
            'Uploading file "' + str(filepath) + '" to bucket "' + str(self.bucket_name) + '", key "' + str(key) + '"'
        )
        client.Bucket(self.bucket_name).upload_file(filepath, key)
        self.logger.info(
            'DONE Upload file "' + str(filepath) + '" to bucket "' + str(self.bucket_name) + '", key "' + str(key) + '"'
        )
        return

    def upload_dir_files(
            self,
            # your local directory path
            dir,
            # s3 target directory path, e.g. /data/sample_docs
            s3_dir,
            # file extension to filter, etc ".pdf"
            file_ext = None,
    ):
        files_in_dir = [
            {'name': f, 'path': os.path.join(dir, f)}
            for f in os.listdir(dir)
            if os.path.isfile(os.path.join(dir, f))
        ]
        if file_ext:
            files_in_dir = [
                d for d in files_in_dir
                if re.match(pattern=".*"+str(file_ext), string=str(d['name']))
            ]
        self.logger.info(
            'Files with extension "' + str(file_ext) + '" in directory "' + str(dir) + '": ' + str(files_in_dir)
        )
        for d in files_in_dir:
            fname, fpath = d['name'], d['path']
            key = s3_dir + '/' + fname
            self.logger.info('Uploading file "' + str(fpath) + '" to s3 "' + str(key) + '"')
            self.upload_file(
                filepath = fpath,
                key = key
            )
        return

    def delete_object(
            self,
            key,
    ):
        session = self.get_boto3_session()
        client = session.client(service_name="s3")
        client.delete_object(Bucket=self.bucket_name, Key=key)
        self.logger.info(
            'DONE delete object key "' + str(key) + '" from bucket "' + str(self.bucket_name) + '"'
        )
        return

    def delete_dir_files(
            self,
            # s3 target directory path, e.g. /data/sample_docs
            s3_dir,
    ):
        objs = self.list_s3_objects(
            folder_prefix = s3_dir,
        )
        self.logger.info('Found objects in s3 dir "' + str(s3_dir) + '"')
        for o in objs:
            key = o['Key']
            self.logger.info(
                'Attempting to delete from bucket "' + str(self.bucket_name) + '", object "' + str(key) + '"'
            )
            self.delete_object(key=key)
        return

    def write_s3_file(
            self,
            data_binary,
            key,
    ):
        session = self.get_boto3_session()
        client = session.client(service_name='s3')
        client.put_object(
            Body = data_binary,
            Bucket = self.bucket_name,
            Key = key,
        )
        return


if __name__ == '__main__':
    Env.set_env_vars_from_file(env_filepath=os.environ["ENV_FILE"])

    bucket_name = 'bigbucket'
    action = os.environ["ACTION"]
    s3_prefix = os.environ["S3_PREFIX"]
    local_files_dir = os.environ.get("LOCAL_FILES_DIR", None)
    fu = AwsS3Utils(
        aws_access_id = os.environ["AWS_ACCESS_ID"],
        aws_access_key = os.environ["AWS_ACCESS_KEY"],
        aws_region = os.environ["AWS_DEFAULT_REGION"],
        bucket_name = bucket_name,
        logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False),
    )

    print('-----------------------------')

    if action == 'list':
        print('Listing s3 prefix "' + str(s3_prefix) + '"...')
        res = fu.list_s3_objects(
            folder_prefix = s3_prefix,
        )
        print('s3 prefix "' + str(s3_prefix) + '" total files ' + str(len(res)))
        [print(d) for d in res]
    elif action == "upload":
        print('Uploading files from local dir "' + str(local_files_dir) + '" to s3 prefix "' + str(s3_prefix) + '"...')
        fu.upload_dir_files(
            dir = local_files_dir,
            s3_dir = s3_prefix,
            file_ext = None,
        )
    elif action == 'delete':
        print('Deleting s3 prefix "' + str(s3_prefix) + '"...')
        fu.delete_dir_files(
            s3_dir = s3_prefix,
        )
    else:
        raise Exception('Unknown action "' + str(action) + '"')

    exit(0)
