import time

from openai import OpenAI

client = OpenAI()


file_upload = client.files.create(file=open("finetune1.jsonl", "rb"), purpose="fine-tune")
fid = file_upload.id
print(f"File uploaded with id: {fid}")


fine_tuning_job = client.fine_tuning.jobs.create(training_file=fid, model="gpt-3.5-turbo")
ft_status = fine_tuning_job.status
print(f"Fine-tuning job created with ID: {fine_tuning_job.id} and status: {ft_status}")


t0 = time.time()
while ft_status != "succeeded":
    fine_tuning_job = client.fine_tuning.jobs.retrieve(fine_tuning_job.id)
    if ft_status != fine_tuning_job.status:
        ft_status = fine_tuning_job.status
        print(f'Fine-tuning job status update: "{ft_status}" at {time.time() - t0:.2f} seconds')
    print(f"Sleeping for 5 seconds...")
    time.sleep(5)
