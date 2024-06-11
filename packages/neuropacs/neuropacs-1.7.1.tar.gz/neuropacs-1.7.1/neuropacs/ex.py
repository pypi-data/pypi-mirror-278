from sdk import Neuropacs

def main():
    # api_key = "your_api_key"
    api_key = "cdXVNIFzEUbSElTpoVoK4SyRrJ7Zj6n6Y6wgApIc"
    server_url = "https://sl3tkzp9ve.execute-api.us-east-2.amazonaws.com/v2/"
    product_id = "PD/MSA/PSP-v1.0"
    result_format = "JSON"


    # PRINT CURRENT VERSION
    # version = Neuropacs.PACKAGE_VERSION

    # INITIALIZE NEUROPACS SDK
    # npcs = Neuropacs.init(server_url, server_url, api_key)
    npcs = Neuropacs(server_url, api_key)

    # CREATE A CONNECTION   
    conn = npcs.connect()
    print(conn)

    # # # # # CREATE A NEW JOB
    order = npcs.new_job()
    print(order)

    # # # # # UPLOAD A DATASET
    # upload = npcs.upload("../dicom_examples/DICOM_small/woo_I0", "test123", order)
    # print(upload)
    datasetID = npcs.upload_dataset("../dicom_examples/06_001", order, order, callback=lambda data: print(data))
    print(datasetID)

    # verUpl = npcs.validate_upload("../dicom_examples/same_name", order, order, callback=lambda data: print(data))
    # print(verUpl)

    # # # START A JOB
    # job = npcs.run_job(product_id, order,order)
    # print(job)

    # # # CHECK STATUS
    # status = npcs.check_status("TEST", "TEST")
    # print(status)

    # # # # GET RESULTS
    # results = npcs.get_results(result_format, "TEST", "TEST")
    # print(results)

    

main()