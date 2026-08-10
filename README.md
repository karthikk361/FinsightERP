\# FinSightERP



A full-stack ERP system for managing products, inventory, sales, user authentication, and business transaction data.



\## Overview



FinSightERP was developed as a software engineering project to demonstrate how a business management system can connect a web frontend, REST APIs, backend business logic, and a relational database.



The system supports core business workflows from product creation through inventory management and sales transactions.



\## Features



\* User authentication

\* Product management

\* Inventory management

\* Sales management

\* Automatic inventory reduction after sales

\* Sales value calculations

\* Dashboard with business metrics

\* PostgreSQL database integration

\* RESTful API

\* Interactive web interface

\* End-to-end workflow testing



\## Technology Stack



\### Backend



\* Python

\* FastAPI

\* SQLAlchemy

\* PostgreSQL



\### Frontend



\* HTML

\* CSS

\* JavaScript



\### Development Tools



\* Git

\* GitHub

\* Swagger / OpenAPI



\## System Architecture



```text

Web Frontend

&#x20;    |

&#x20;    v

FastAPI REST API

&#x20;    |

&#x20;    v

Business Logic

&#x20;    |

&#x20;    v

PostgreSQL Database

```



\## Core Workflow



```text

User Login

&#x20;   |

&#x20;   v

Dashboard

&#x20;   |

&#x20;   +----> Products

&#x20;   |

&#x20;   +----> Inventory

&#x20;   |

&#x20;   +----> Sales

&#x20;             |

&#x20;             v

&#x20;      Inventory Updated

&#x20;             |

&#x20;             v

&#x20;      Dashboard Updated

```



\## API Endpoints



| Method | Endpoint     | Description                |

| ------ | ------------ | -------------------------- |

| GET    | `/`          | API status                 |

| POST   | `/login`     | User authentication        |

| GET    | `/products`  | Retrieve products          |

| POST   | `/products`  | Create product             |

| GET    | `/inventory` | Retrieve inventory         |

| POST   | `/inventory` | Add inventory              |

| GET    | `/sales`     | Retrieve sales             |

| POST   | `/sales`     | Create sale                |

| GET    | `/dashboard` | Retrieve dashboard metrics |



\## Project Structure



```text

FinSightERP/

│

├── backend/

│   ├── main.py

│   ├── database.py

│   └── test\_db.py

│

├── frontend/

│   └── index.html

│

├── .gitignore

└── README.md

```



\## Testing



The system was tested through end-to-end business workflows including:



\* User login

\* Product creation

\* Inventory creation

\* Sales transactions

\* Automatic inventory reduction

\* Sales value calculation

\* Dashboard updates

\* Frontend-to-backend communication

\* Backend-to-database communication



\## Project Purpose



The project demonstrates practical software engineering concepts including REST API development, relational database integration, backend business logic, frontend development, authentication, and end-to-end system testing.



