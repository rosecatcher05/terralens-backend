FROM python:3.9

WORKDIR /code

# Copy requirements and install uvicorn explicitly along with everything else
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uvicorn && \
    pip install --no-cache-dir -r /code/requirements.txt

COPY . /code

# Use explicit python module invocation to avoid PATH issues
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]