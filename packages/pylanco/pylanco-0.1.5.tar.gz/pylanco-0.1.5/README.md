# pylanco <a href="https://pypi.org/project/pylanco/">[0.1.5]</a>

## Usage:
> Update conda.yaml with the following: 
```yaml
- pylanco==0.1.5
```
<details>
  <summary>ERP</summary>
  
```python
from pylanco import ERP
```
```python
login_secret = Vault().get_secret("") # Lacking information due to security reasons
LOGIN_TOKEN = login_secret[""]
COMPANY_ID = login_secret[""]

url_secret = Vault().get_secret("") # Lacking information due to security reasons
BASE_URL = url_secret[""]
```

## Table of Contents
- [get_customers](#get_customers)
- [get_customer](#get_customer)
- [get_customer_categories](#get_customer_categories)
- [get_customer_groups](#get_customer_groups)
- [get_employees](#get_employees)
- [get_employee](#get_employee)
- [get_employee_groups](#get_employee_groups)
- [get_employee_teams](#get_employee_teams)
- [get_product_type_categories](#get_product_type_categories)
- [get_product_types](#get_product_types)
- [get_product_type](#get_product_type)
- [get_customer_invoicing_report](#get_customer_invoicing_report)
- [get_employee_invoicing_report](#get_employee_invoicing_report)
- [get_work_session_assignments](#get_work_session_assignments)

---

### get_customers
> */customers*

```python
ERP.get_customers(BASE_URL, COMPANY_ID, LOGIN_TOKEN) # Returns a list of customers in JSON format
```
<details>
  <summary>Details</summary>

>  
>  ```python
>.name(archived=None/True/False) # Returns a list of customer by customer name
>```
> **Note:**
> Archived status is set to None by default.
>
>```python
>.id(archived=None/True/False) # Returns a list of customers by customer ID
>```
> **Note:**
> Archived status is set to None by default.
</details>

### get_customer
> */customers/{customer_id}*

```python
ERP.get_customer(BASE_URL, COMPANY_ID, LOGIN_TOKEN, customer_id) # Returns customer data in JSON format
```
<details>
<summary>Details</summary>
  
> **Note:**
> Loops through all customers if customer_id parameter is a list
>  
>```python
>.name() # Returns name of the customer
>```
>
>```python
>.archived() # Returns archived status of the customer
>```
>
>```python
>.group_names() # Returns group names of the customer
>```
>
>```python
>.group_ids() # Returns group IDs of the customer
>```
</details>

### get_customer_categories
> */customers/categories*

```python
ERP.get_customer_categories(BASE_URL, COMPANY_ID, LOGIN_TOKEN) # Returns customer categories data in JSON format
```

<details>
  <summary>Details</summary>

>  
>```python
>.customers(category=name/ID) # Returns customer IDs by category name or ID
>```
>
>```python
>.employees(category=name/ID) # Returns employee IDs by category name or ID
>```
>
>```python
>.category(category=name/ID) # Returns category by name or ID
>```
</details>


### get_customer_groups
> */customers/groups*

```python
ERP.get_customer_groups(BASE_URL, COMPANY_ID, LOGIN_TOKEN) # Returns customer groups data in JSON format
```

<details>
  <summary>Details</summary>

>```python
>.customers(group=name/ID) # Returns customer IDs by group name or ID
>```
>
>```python
>.group(group=name/ID) # Returns customer group by name or ID
>```
</details>

### get_employees
> */employees*

```python
ERP.get_employees(BASE_URL, COMPANY_ID, LOGIN_TOKEN) # Returns employees data in JSON format
```

<details>
  <summary>Details</summary>

>```python
>.name() # Returns list of employee names
>```
>
>```python
>.id() # Returns list of employee IDs
>```
</details>

### get_employee
> */employees/{employee_id}*

```python
ERP.get_employee(BASE_URL, COMPANY_ID, LOGIN_TOKEN, employee_id) # Returns employee data in JSON format
```

<details>
  <summary>Details</summary>
  
> **Note:**
> Loops through all employee IDs if employee_id parameter is a list
>
>```python
>.name() # Returns name of the employee
>```
>
>```python
>.title() # Returns title of the employee
>```
>
>```python
>.email() # Returns email of the employee
>```
>
>```python
>.group_names() # Returns a list of the group names of the employee
>```
>
>```python
>.group_ids() # Returns a list of group IDs of the employee
>```
</details>

### get_employee_groups
> */employee/groups*

```python
ERP.get_employee_groups(BASE_URL, COMPANY_ID, LOGIN_TOKEN) # Returns employee groups data in JSON format
```

<details>
  <summary>Details</summary>

>```python
>.employees(group=name/ID) # Returns list of employee IDs by group name or ID
>```
>
>```python
>.group(group=name/ID) # Returns employee group data by name or ID
>```
</details>

### get_employee_teams
> */employee/teams*

```python
ERP.get_employee_teams(BASE_URL, COMPANY_ID, LOGIN_TOKEN) # Returns employee teams data in JSON format
```

<details>
  <summary>Details</summary>

>```python
>.employees(team=name/ID) # Returns a list of employee IDs by team name or ID
>```
>
>```python
>.foremen(team=name/ID) # Returns a list of foreman IDs by team name or ID
>```
>
>```python
>.team(team=name/ID) # Returns team data by name or ID
>```
</details>

### get_product_type_categories
> */product_types/categories*

```python
ERP.get_product_type_categories(BASE_URL, COMPANY_ID, LOGIN_TOKEN) # Returns product type categories data in JSON format
```

<details>
  <summary>Details</summary>

>```python
>.product(category=name/ID) # Returns list of product type IDs by category name or ID
>```
</details>

### get_product_types
> */product_types*

```python
ERP.get_product_types(BASE_URL, COMPANY_ID, LOGIN_TOKEN) # Returns product types data in JSON format
```

### get_product_type
> */product_types/{product_type_id}*

```python
ERP.get_product_type(BASE_URL, COMPANY_ID, LOGIN_TOKEN, product_type_id) # Returns product type data in JSON format
```
<details>
  <summary>Details</summary>
  
> **Note:**
> Loops through all product type IDs if product_type_id parameter is a list
>
>```python
>.name() # Returns name of product type
>```
</details>

### get_customer_invoicing_report
> */report/customer_invoicing*

```python
ERP.get_customer_invoicing_report(BASE_URL, COMPANY_ID, LOGIN_TOKEN, term_start, term_end, customer_ids, employee_ids, project_template_ids, project_task_template_ids, product_type_ids, sessions_cost, contract_cost, services_cost, products_cost, internal_cost, internal_product_cost) # Returns customer invoicing report data in JSON format
```
<details>
  <summary>Details</summary>
  
> **Note:**
> - Only the following parameters are mandatory: BASE_URL, COMPANY_ID, LOGIN_TOKEN, term_start, term_end
> - ID parameters can be passed as string or a list
> - All cost parameters are boolean values, and are set to False by default
</details>

### get_employee_invoicing_report
> */report/employee_invoicing*

```python
ERP.get_employee_invoicing_report(BASE_URL, COMPANY_ID, LOGIN_TOKEN, term_start, term_end, employee_ids, customer_ids, team_id, product_type_ids) # Returns employee invoicing report data in JSON format
```
<details>
  <summary>Details</summary>

> **Note:**
> - Only the following parameters are mandatory: BASE_URL, COMPANY_ID, LOGIN_TOKEN, term_start, term_end
> - ID parameters can be passed as string or a list
</details>

### get_work_session_assignments
> */work_session/assignments*

```python
ERP.get_work_session_assignments(BASE_URL, COMPANY_ID, LOGIN_TOKEN, start_date, end_date, employee_id, customer_id, ids, limit, offset) # Returns work session assignments data in JSON format
```
<details>
  <summary>Details</summary>

> **Note:**
> - Only the following parameters are mandatory: BASE_URL, COMPANY_ID, LOGIN_TOKEN, term_start, term_end
> - ID parameters can be passed as string or a list
> - Limit is set to 100 by default
> - Offset is set to 0 by default
>
> ```python
>  .name(name) # Returns work session assignments by assignment name
> ```

</details
</details>
