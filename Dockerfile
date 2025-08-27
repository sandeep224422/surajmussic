# ✅ Latest stable Python 3.10 + Node.js 20 image use karo
FROM nikolaik/python-nodejs:python3.10-nodejs20

# ✅ Update & install ffmpeg
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy project files
COPY . /app/
WORKDIR /app/

# ✅ Upgrade pip
RUN python -m pip install --no-cache-dir --upgrade pip

# ✅ Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Start command
CMD ["bash", "start"]
