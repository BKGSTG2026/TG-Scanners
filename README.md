## uPASS RFID to MSSQL Bridge

This document provides the architectural overview and configuration steps for an industrial IoT solution using a Raspberry Pi to bridge Nedap uPASS Go scanners with a remote Microsoft SQL Server.
**Prerequisites**:
   - Hardware: Raspberry Pi (Model 3B+, 4, or 5).
   - Operating System: Raspberry Pi OS (64-bit recommended).
   - Network: Ethernet or stable Wi-Fi with access to the scanners (Port 10001) and the SQL Server (Port 1433).

#### Installation and Configuration
1. Install Node-RED

The following script installs Node.js, npm, and Node-RED, while also adding specific Raspberry Pi optimizations and the systemd service files.

   ```bash 
   bash <(curl -sL https://raw.githubusercontent.com/node-red/linux-installers/master/deb/update-nodejs-and-nodered)
   ```

2. Install MSSQL Node

The node-red-contrib-mssql-plus library is used to provide a pure JavaScript implementation of the TDS protocol. This eliminates the need for official Microsoft ODBC drivers which are often difficult to configure on ARM-based Linux systems.
   ```bash
   cd ~/.node-red
   npm install node-red-contrib-mssql-plus
   ```

**System Management (systemd)**

Node-RED is managed as a background service. This allows the application to start automatically upon power-up and recover from software crashes.
Standard Commands
Command	Description
sudo systemctl enable nodered.service	Configure the application to start on boot.
node-red-start	Start the service and open the log stream.
node-red-stop	Gracefully shut down the application.
node-red-log	View the live output for debugging scanner connections.
sudo systemctl status nodered.service	Verify if the service is active or faulted.
Version Control and Git Integration

To manage the application as plain text and maintain a history of changes, the Node-RED "Projects" feature should be utilized.
Enabling Projects

    Open the settings file: nano ~/.node-red/settings.js.

    Locate the editorTheme property.

    Set projects: { enabled: true }.

    Restart Node-RED using node-red-restart.

Once enabled, the entire flow configuration is stored as a JSON file within a local Git repository on the Pi, allowing for standard git push and git pull operations to move the logic between development and production environments.
Technical Architecture
Component Breakdown

    Input Layer: Eight TCP In nodes act as listeners or clients for the uPASS Go readers. Each node is assigned a unique Topic (e.g., Gate_01) to identify the data source.

    Processing Layer: A Function node cleans the raw HEX buffer and converts it into a structured JavaScript object.

    Throttling Layer: A Delay node configured for "Rate Limit" ensures that a single vehicle stopped in front of a reader does not flood the database with duplicate entries.

    Persistence Layer: An MSSQL node in "Statement" mode executes the INSERT command into the remote database.

SQL Database Schema

The remote MSSQL server should be configured with a table similar to the following to ensure data compatibility:
SQL

CREATE TABLE Scans (
    EntryID INT IDENTITY(1,1) PRIMARY KEY,
    TagID VARCHAR(64) NOT NULL,
    ScannerName VARCHAR(32),
    CaptureTime DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET()
);

Portability and Testing

To migrate the solution from a test environment to a production environment:

    Export the Flow JSON from the test Pi.

    Import the JSON into the production Pi.

    Update the Environment Variables (or Global Context) for the production SQL Server IP and credentials.

    Replace the "Inject" manual test nodes with the live "TCP In" nodes connected to the physical uPASS IP addresses.