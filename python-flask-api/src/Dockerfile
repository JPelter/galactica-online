FROM python:3.11
# Install Microsoft ODBC Driver for SQL Server on Linux
RUN apt-get update && apt-get install -y gnupg2 curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17
# IN THE FUTURE, NEED TO UPGRADE TO msodbcsql18!

# NOW CREATE APP FOLDER, COPY CODE, INSTALL PYTHON DEPDENCIES, AND RUN THE APP
WORKDIR /app
COPY server.py .
COPY auth_routes.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "server.py" ]