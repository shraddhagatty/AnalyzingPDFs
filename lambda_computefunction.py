#
# Python program to open and process a PDF file, extracting
# all numeric values from the document. The goal is to tally
# the first significant (non-zero) digit of each numeric
# value, and save the results to a text file. This will
# allow checking to see if the results follow Benford's Law,
# a common method for detecting fraud in numeric data.
#
# https://en.wikipedia.org/wiki/Benford%27s_law
# https://chance.amstat.org/2021/04/benfords-law/
#

import json
import boto3
import os
import uuid
import base64
import pathlib
import datatier
import urllib.parse
import string

from configparser import ConfigParser
from pypdf import PdfReader

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: proj03_compute**")
    
    # 
    # in case we get an exception, set this to a default
    # filename so we can write an error message if need
    # be:
    #
    local_results_file = "/tmp/results.txt"
    bucketkey_results_file = ""
    
    #
    # setup AWS based on config file:
    #
    config_file = 'config.ini'
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
    
    configur = ConfigParser()
    configur.read(config_file)
    
    #
    # configure for S3 access:
    #
    s3_profile = 's3readwrite'
    boto3.setup_default_session(profile_name=s3_profile)
    
    bucketname = configur.get('s3', 'bucket_name')
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucketname)
    
    #
    # configure for RDS access
    #
    rds_endpoint = configur.get('rds', 'endpoint')
    rds_portnum = int(configur.get('rds', 'port_number'))
    rds_username = configur.get('rds', 'user_name')
    rds_pwd = configur.get('rds', 'user_pwd')
    rds_dbname = configur.get('rds', 'db_name')
    
    #
    # this function is event-driven by a PDF being
    # dropped into S3. The bucket key is sent to 
    # us and obtain as follows:
    #
    bucketkey = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    print("bucketkey:", bucketkey)
      
    extension = pathlib.Path(bucketkey).suffix
    
    if extension != ".pdf" : 
      raise Exception("expecting S3 document to have .pdf extension")
    
    bucketkey_results_file = bucketkey[0:-4] + ".txt"
    
    print("bucketkey results file:", bucketkey_results_file)
    print("local results file:", local_results_file)
      
    #
    # download PDF from S3:
    #
    print("**DOWNLOADING '", bucketkey, "'**")

    local_pdf = "/tmp/data.pdf"
    
    bucket.download_file(bucketkey, local_pdf)

    #
    # open pdf file:
    #
    print("**PROCESSING local PDF**")
    
    reader = PdfReader(local_pdf)
    number_of_pages = len(reader.pages)
    
    #
    # for each page, extract text, split into words,
    # and see which words are numeric values:
    #
    for i in range(0, number_of_pages):
      page = reader.pages[i]
      text = page.extract_text()
      words = text.split()
      print("** Page", i, ", text length", len(text), ", num words", len(words))
      for word in words:
        word = word.translate(str.maketrans('', '', string.punctuation))
        if word.isnumeric():
          #
          # find the first non-zero digit and count it:
          #
          #
          # TODO
          #
          pass


    
    #
    # write the results to local results file:
    #
    outfile = open(local_results_file, "w")
    outfile.write("**RESULTS**\n")
    outfile.write(str(number_of_pages))
    outfile.write(" pages\n")


    #
    # TODO: Write the 10 counts
    #
    

    outfile.close()
    
    #
    # upload the results file to S3:
    #
    print("**UPLOADING to S3 file", bucketkey_results_file, "**")

    bucket.upload_file(local_results_file,
                       bucketkey_results_file,
                       ExtraArgs={
                         'ACL': 'public-read',
                         'ContentType': 'text/plain'
                       })
    
    # 
    # The last step is to update the database to change
    # the status of this job, and store the results
    # bucketkey:

    #
    # TODO: open connection, and update job in database.
    # Change the status to 'completed', and update the
    # resultsfilekey.
    #



    #
    # done!
    #
    # respond in an HTTP-like way, i.e. with a status
    # code and body in JSON format:
    #
    print("**DONE, returning success**")
    
    return {
      'statusCode': 200,
      'body': json.dumps("success")
    }
    

  #
  # on an error, try to upload error message to S3:
  #
  except Exception as err:
    print("**ERROR**")
    print(str(err))
    
    outfile = open(local_results_file, "w")

    outfile.write(str(err))
    outfile.write("\n")
    outfile.close()
    
    if bucketkey_results_file == "": 
      #
      # we can't upload the error file:
      #
      pass
    else:
      # 
      # upload the error file to S3
      #
      print("**UPLOADING**")
      #
      bucket.upload_file(local_results_file,
                         bucketkey_results_file,
                         ExtraArgs={
                           'ACL': 'public-read',
                           'ContentType': 'text/plain'
                         })

    #
    # update jobs row in database:
    #
    #
    # TODO: open connection, update job in database
    # Change the status to 'error', and update the
    # resultsfilekey.
    #



    #
    # done, return:
    #    
    return {
      'statusCode': 400,
      'body': json.dumps(str(err))
    }
