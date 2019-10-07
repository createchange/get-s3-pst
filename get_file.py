import boto3

conn = boto3.client('s3', region_name='us-east-2')

def search_for_file():
    '''
    Performs a query and returns a list of the files matching
    '''
    search_results = []
    
    while True:
        pst_file = input("Whose PST file do you want to create a link for?\n> ").lower()
        if pst_file != "":
            break
        else:
            print("You must make a query. Please try again.\n")

    for key in conn.list_objects(Bucket='veeam-backup-prod', Prefix='')['Contents']:
        if pst_file in key['Key'].lower():
            search_results.append(key['Key'])
    if not search_results:
        print("No results - please try again...\n")

    return search_results

def get_selection(search_results):
    while True:
        print("\nSearch Results:\n")
        for result in search_results:
            print("[" + str(search_results.index(result)) + "] " + str(result))
        selection = int(input("\nPlease input the number associated with the PST:\n> "))
        try:
            return search_results[selection]
        except:
            print("Invalid selection, please try again.\n")
    

# Main
print("===== S3 Presigned URL Generator =====\n")

while True:
    search_results = search_for_file()
    if search_results:
        break

selection = get_selection(search_results)

presigned_url = conn.generate_presigned_url('get_object', Params = {'Bucket': 'veeam-backup-prod', 'Key': selection}, ExpiresIn = 600)
print("\nPresigned URL:\n%s" % presigned_url)
