# AWS-S3-File-Mover-Mananger
A lambda for sorting file by extension and sending matching extension types to specific buckets


--------
Summary
--------
This project was created to manage files uploaded to an S3 bucket. The lambda is meant to be used with an S3 trigger on a target bucket. Once triggered, the lambda will look for specific file extentions (found in the 'extentions' dictionary') and move matching files to a designated bucket/folder for those types of files. Any files not matching one of those extention types will be deleted.

