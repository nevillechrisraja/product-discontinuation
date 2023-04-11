# Product Discontinuation

### Project Steps
1. Extract source data from AWS Redshift DB
2. Perform data preprocessing
3. Perform ML model training and save the model in AWS S3
4. Load the trained model from S3 and perform ML prediction
5. Push prediction results to AWS Redshift DB

### To run using Docker containers

1. Build docker image.

    _'docker build -t <<user.name>>/product-discontinuation .'_

2. Run container.

    _'docker run --name project-product-discontinuation <<user.name>>/product-discontinuation -r TRUE'_

Note:
1. If the container name already exists, then use the below command to remove the container before issuing docker run command.

    _'docker rm project-product-discontinuation'_

### Output

1. The output are stored in the table 'catalogue_discontinued' in the 'data_science' database.

2. The output contains the fields Id and the predicted Discontinued status with values as True/False.

### Progress

Code work is carried out on separate feature branches, then merged to Dev.
