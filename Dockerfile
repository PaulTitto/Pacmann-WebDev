# Menggunakan base image yang sesuai
FROM python:3.9

# Menentukan direktori kerja di dalam container
WORKDIR /app

# Menyalin (COPY) data aplikasi ke dalam image
COPY . /app

# Menginstal dependensi dari file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Menjalankan server Flask
CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0"]
