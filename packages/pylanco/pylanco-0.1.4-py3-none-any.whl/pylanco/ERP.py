import requests
import robocorp.log

class ERP:
    @staticmethod
    def get_customers(BASE_URL, COMPANY_ID, LOGIN_TOKEN):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/customers?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return Customers(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

    @staticmethod
    def get_customer(BASE_URL, COMPANY_ID, LOGIN_TOKEN, customer_id):
        try:
            if isinstance(customer_id, list):
                customers = []
                for id in customer_id:
                    with robocorp.log.suppress_variables():
                        url = f"{BASE_URL}/customers/{id}?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                        response = requests.get(url)
                        response.raise_for_status()
                        customers.append(Customer(response.json()))
                return customers
            else:
                with robocorp.log.suppress_variables():
                    url = f"{BASE_URL}/customers/{customer_id}?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                    response = requests.get(url)
                    response.raise_for_status()
                    return Customer(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_customer_categories(BASE_URL, COMPANY_ID, LOGIN_TOKEN):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/customers/categories?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return Categories(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_customer_groups(BASE_URL, COMPANY_ID, LOGIN_TOKEN):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/customers/groups?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return Groups(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_employees(BASE_URL, COMPANY_ID, LOGIN_TOKEN):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/employees?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return Employees(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
    
    @staticmethod
    def get_employee(BASE_URL, COMPANY_ID, LOGIN_TOKEN, employee_id):
        try:
            if isinstance(employee_id, list):
                employees = []
                for id in employee_id:
                    with robocorp.log.suppress_variables():
                        url = f"{BASE_URL}/employees/{id}?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                        response = requests.get(url)
                        response.raise_for_status()
                        employees.append(Employee(response.json()))
                return employees
            else:    
                with robocorp.log.suppress_variables():
                    url = f"{BASE_URL}/employees/{employee_id}?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                    response = requests.get(url)
                    response.raise_for_status()
                    return Employee(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e            
        
    @staticmethod
    def get_employee_groups(BASE_URL, COMPANY_ID, LOGIN_TOKEN):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/employee/groups?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return EmployeeGroups(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_employee_teams(BASE_URL, COMPANY_ID, LOGIN_TOKEN):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/employee/teams?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return EmployeeTeams(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_product_type_categories(BASE_URL, COMPANY_ID, LOGIN_TOKEN):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/product_types/categories?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return ProductTypes(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_product_types(BASE_URL, COMPANY_ID, LOGIN_TOKEN):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/product_types?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_product_type(BASE_URL, COMPANY_ID, LOGIN_TOKEN, product_type_id):
        try:
            if isinstance(product_type_id, list):
                product_types = []
                for id in product_type_id:
                    with robocorp.log.suppress_variables():
                        url = f"{BASE_URL}/product_types/{product_type_id}?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                        response = requests.get(url)
                        response.raise_for_status()
                        product_types.append(ProductType(response.json()))
                    return product_types
            else:
                with robocorp.log.suppress_variables():
                    url = f"{BASE_URL}/product_types/{product_type_id}?company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                    response = requests.get(url)
                    response.raise_for_status()
                    return ProductType(response.json())
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_customer_invoicing_report(BASE_URL, COMPANY_ID, LOGIN_TOKEN, term_start, term_end, customer_ids=None, employee_ids=None, project_template_ids=None, project_task_template_ids=None, product_type_ids=None, sessions_cost=False, contract_cost=False, services_cost=False, products_cost=False, internal_cost=False, internal_product_cost=False):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/report/customer_invoicing?selection%5Bterm_start%5D={term_start}&selection%5Bterm_end%5D={term_end}"

                def add_ids_to_url(param_name, param_value):
                    if isinstance(param_value, (int, str)):
                        return f"&selection%5B{param_name}%5D%5B%5D={param_value}"
                    elif isinstance(param_value, list):
                        return ''.join(f"&selection%5B{param_name}%5D%5B%5D={str(id_)}" for id_ in param_value)
                    return ''

                if customer_ids is not None:
                    url += add_ids_to_url('customer_ids', customer_ids)
                
                if employee_ids is not None:
                    url += add_ids_to_url('employee_ids', employee_ids)

                if project_template_ids is not None:
                    url += add_ids_to_url('project_template_ids', project_template_ids)
                
                if project_task_template_ids is not None:
                   url += add_ids_to_url('project_task_temaplte_ids', project_task_template_ids)
                
                if product_type_ids is not None:
                    url += add_ids_to_url('product_type_ids', product_type_ids)

                url += f"&selection%5Bsessions_cost%5D={sessions_cost}&selection%5Bcontract_cost%5D={contract_cost}&selection%5Bservices_cost%5D={services_cost}&selection%5Bproducts_cost%5D={products_cost}&selection%5Binternal_cost%5D={internal_cost}&selection%5Binternal_product_cost%5D={internal_product_cost}"
                url += f"&company_id={COMPANY_ID}&token={LOGIN_TOKEN}"

                response = requests.get(url)
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_employee_invoicing_report(BASE_URL, COMPANY_ID, LOGIN_TOKEN, term_start, term_end, employee_ids=None, customer_ids=None, team_id=None, product_type_ids=None):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/report/employee_invoicing?selection%5Bterm_start%5D={term_start}&selection%5Bterm_end%5D={term_end}"

                def add_ids_to_url(param_name, param_value):
                    if isinstance(param_value, (int, str)):
                        return f"&selection%5B{param_name}%5D%5B%5D={param_value}"
                    elif isinstance(param_value, list):
                        return ''.join(f"&selection%5B{param_name}%5D%5B%5D={str(id_)}" for id_ in param_value)
                    return ''
                
            if employee_ids is not None:
                url += add_ids_to_url('employee_ids', employee_ids)

            if customer_ids is not None:
                url += add_ids_to_url('customer_ids', customer_ids)
            
            if team_id is not None:
                url += add_ids_to_url('team_id', team_id)
            
            if product_type_ids is not None:
                url += add_ids_to_url('product_type_ids', product_type_ids)
        
            url += f"&company_id={COMPANY_ID}&token={LOGIN_TOKEN}"

            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError("Error") from e
        
    @staticmethod
    def get_work_session_assignments(BASE_URL, COMPANY_ID, LOGIN_TOKEN, start_date, end_date, employee_id=None, customer_id=None, ids=None, limit=100, offset=0):
        try:
            with robocorp.log.suppress_variables():
                url = f"{BASE_URL}/work_session/assignments?start_date={start_date}&end_date={end_date}&limit={limit}&offset={offset}"
                
                def add_ids_to_url(param_name, param_value):
                    if isinstance(param_value, (int, str)):
                        return f"&{param_name}%5B%5D={param_value}"
                    elif isinstance(param_value, list):
                        return ''.join(f"&{param_name}%5B%5D={str(id_)}" for id_ in param_value)
                    return ''

                if employee_id is not None:
                    url += add_ids_to_url('employee_id', employee_id)
                
                if customer_id is not None:
                    url += add_ids_to_url('customer_id', customer_id)
                
                if ids is not None:
                    url += add_ids_to_url('ids', ids)
                
                url += f"&company_id={COMPANY_ID}&token={LOGIN_TOKEN}"
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
        except requests.RequestException as e:
            raise RuntimeError("Error") from e

class Customers:
    def __init__(self, customers):
        self.customers = customers

    def id(self, archived=None):
        return [customer['id'] for customer in self._filter_customers(archived)]

    def name(self, archived=None):
        return [customer['name'] for customer in self._filter_customers(archived)]

    def _filter_customers(self, archived):
        if archived is None:
            return self.customers
        if archived:
            return [customer for customer in self.customers if customer.get('archived', False)]
        else:
            return [customer for customer in self.customers if not customer.get('archived', False)]

    def __repr__(self):
        return str(self.customers)

class Customer:
    def __init__(self, customer_data):
        self.customer_data = customer_data

    def name(self):
        return self.customer_data['name']

    def archived(self):
        return self.customer_data.get('archived', False)
    
    def group_names(self):
        return self.customer_data.get('group_names')
    
    def group_ids(self):
        return self.customer_data.get('group_ids')

    def __repr__(self):
        return str(self.customer_data)
    
class Categories:
    def __init__(self, categories):
        self.categories = categories

    def customers(self, category=None):
        if category is None:
            raise ValueError("Category name or ID must be provided")
        if str(category).isdigit():
            return self._filter_categories_by_id(int(category))[0]['customer_ids']
        else:
            return self._filter_categories_by_name(category)[0]['customer_ids']
    
    def employees(self, category=None):
        if category is None:
            raise ValueError("Category name or ID must be provided")
        if str(category).isdigit():
            return self._filter_categories_by_id(int(category))[0]['employee_ids']
        else:
            return self._filter_categories_by_name(category)[0]['employee_ids']
        
    def category(self, category=None):
        if category is None:
            raise ValueError("Category name or ID must be provided")
        if str(category).isdigit():
            filtered_categories = self._filter_categories_by_id(int(category))
            if not filtered_categories:
                raise ValueError(f"No customer_category with ID '{category}' in customer categories")
            return filtered_categories[0]
        else:
            filtered_categories = self._filter_categories_by_name(category.lower())
            if not filtered_categories:
                raise ValueError(f"No customer category with name '{category}' in customer categories")
            return filtered_categories[0]
    
    def _filter_categories_by_name(self, name):
        return [category for category in self.categories if category.get('name', '').lower() == name]
    
    def _filter_categories_by_id(self, category_id):
        return [category for category in self.categories if category.get('id') == category_id]
    
    def __repr__(self):
        return str(self.categories)

class Groups:
    def __init__(self, groups):
        self.groups = groups

    def customers(self, group=None):
        if group is None:
            raise ValueError("Group name or ID must be provided")
        if str(group).isdigit():
            return self._filter_groups_by_id(int(group))[0]['customer_ids']
        else:
            return self._filter_groups_by_name(group.lower())[0]['customer_ids']
        
    def group(self, group=None):
        if group is None:
            raise ValueError("Group name or ID must be provided")
        if str(group).isdigit():
            filtered_groups = self._filter_groups_by_id(int(group))
            if not filtered_groups:
                raise ValueError(f"No customer group with ID '{group}' in customer groups")
            return filtered_groups[0]
        else:
            filtered_groups = self._filter_groups_by_name(int(group))
            if not filtered_groups:
                raise ValueError(f"No customer group with name '{group}' in customer groups")
            return filtered_groups[0]

    def _filter_groups_by_name(self, name):
        return [group for group in self.groups if group.get('name', '').lower() == name]

    def _filter_groups_by_id(self, group_id):
        return [group for group in self.groups if group.get('id') == group_id]

    def __repr__(self):
        return str(self.groups)
    
class Employees:
    def __init__(self, employees):
        self.employees = employees

    def id(self):
        return [employee['id'] for employee in self.employees]
    
    def name(self):
        return [employee['name'] for employee in self.employees]
    
    def __repr__(self):
        return str(self.employees)
    
class Employee:
    def __init__(self, employee_data):
        self.employee_data = employee_data

    def name(self):
        return self.employee_data['name']
    
    def title(self):
        return self.employee_data['title']
    
    def email(self):
        return self.employee_data['email']
    
    def group_names(self):
        return self.employee_data.get('group_names')
    
    def group_ids(self):
        return self.employee_data.get('group_ids')
    
    def __repr__(self):
        return str(self.employee_data)

class EmployeeGroups:
    def __init__(self, groups):
        self.groups = groups
    
    def employees(self, group=None):
        if group is None:
            raise ValueError("Group name or ID must be provided")
        if str(group).isdigit():
            return self._filter_groups_by_id(int(group))[0]['employee_ids']
        else:
            return self._filter_groups_by_name(group.lower())[0]['employee_ids']
        
    def group(self, group=None):
        if group is None:
            ValueError("Group name or ID must be provided")
        if str(group).isdigit():
            filtered_groups = self._filter_groups_by_id(int(group))
            if not filtered_groups:
                raise ValueError(f"No employee group with ID '{group}' in employee groups")
            return filtered_groups[0]
        else:
            filtered_groups = self._filter_groups_by_name(group.lower())
            if not filtered_groups:
                raise ValueError(f"No employee group with name '{group}' in employee groups")
            return filtered_groups[0]
    
    def _filter_groups_by_name(self, name):
        return [group for group in self.groups if group.get('name', '').lower() == name]
    
    def _filter_groups_by_id(self, group_id):
        return [group for group in self.groups if group.get('id') == group_id]

    def __repr__(self):
        return str(self.groups)
    
class EmployeeTeams:
    def __init__(self, teams):
        self.teams = teams

    def employees(self, team=None):
        if team is None:
            raise ValueError("Team name or ID must be provided")
        if str(team).isdigit():
            return self._filter_teams_by_id(int(team))[0]['employee_ids']
        else:
            return self._filter_teams_by_name(team.lower())[0]['employee_ids']
        
    def foremen(self, team=None):
        if team is None:
            raise ValueError("Team name or ID must be provided")
        if str(team).isdigit():
            return self._filter_teams_by_id(int(team))[0]['foreman_ids']
        else:
            return self._filter_teams_by_name(team.lower())[0]['foreman_ids']
    
    def team(self, team=None):
        if team is None:
            raise ValueError("Team name or ID must be provided")
        if str(team).isdigit():
            filtered_teams =  self._filter_teams_by_id(int(team))
            if not filtered_teams:
                raise ValueError(f"No employee team with ID '{team}' in employee teams")
            return filtered_teams[0]
        else:
            filtered_teams = self._filter_teams_by_name(team.lower())
            if not filtered_teams:
                raise ValueError(f"No employee team with name '{team}' in employee teams")
            return filtered_teams[0]
    
    def _filter_teams_by_name(self, name):
        return [team for team in self.teams if team.get('name', '').lower() == name]
    
    def _filter_teams_by_id(self, team_id):
        return [team for team in self.teams if team.get('id') == team_id]

    def __repr__(self):
        return str(self.teams)
    
class ProductTypes:
    def __init__(self, producttypes):
        self.producttypes = producttypes

    def product(self, product):
        if product is None:
            raise ValueError("Product name or ID must be provided")
        if str(product).isdigit():
            return self._filter_types_by_id(int(product))
        else:
            return self._filter_types_by_name(product.lower())
            
    def _filter_types_by_name(self, name):
        for type in self.producttypes:
            if type.get('name', '').lower() == name:
                return type.get('product_type_ids', [])
        return []

    def _filter_types_by_id(self, type_id):
        for type in self.producttypes:
            if type.get('id') == type_id:
                return type.get('product_type_ids', [])
        return []

    def __repr__(self):
        return str(self.producttypes)
    
class ProductType:
    def __init__(self, producttype):
        self.producttype = producttype

    def name(self):
        return self.producttype['name']

    def __repr__(self):
        return str(self.producttype)