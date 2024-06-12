"""
Define an interface for parsing azure template and its parameter files.
"""
import copy
import glob
import re
import os
import inspect
import ast
import traceback
import hcl2
from processor.logging.log_handler import getlogger
from processor.templates.base.template_parser import TemplateParser
from processor.helper.file.file_utils import exists_file, exists_dir
from processor.templates.terraform.helper.function.terraform_functions import default_functions
from processor.templates.terraform.helper.expression.terraform_expressions import expression_list
from processor.helper.json.json_utils import json_from_file, json_from_string
from processor.helper.hcl.hcl_utils import hcl_to_json
from processor.templates.terraform.helper.module_parser import ModuleParser

logger = getlogger()

class TerraformTemplateParser(TemplateParser):
    """
    Terraform Parser class for process terraform template
    """
    def __init__(self, template_file, tosave=False, **kwargs):
        super().__init__(template_file, tosave=False, **kwargs)
        self.imports = []
        self.schema_filter = {
            "var" : self.process_variable,
            "data" : self.process_data,
            "other" : self.process_other,
            "local" : self.process_locals,
        }
        self.default_gparams = kwargs.get("default_gparams", {})
        self.gdata = {}
        self.locals = kwargs.get("locals", {})
        self.resource = {}
        self.module_params = {
            "module" : {}
        }
        self.temp_params = {}
        self.count = None
        self.process_module = kwargs.get("process_module", False)
        self.replace_values = {
            "true" : True,
            "false" : False,
            "True" : True,
            "False" : False,
            "&&" : "and",
            "||" : "or",
            "None" : None,
            "!" : "not",
        }
        self.replace_value_str = ["and", "or", "not"]
        self.template_file_list = [self.template_file]
        self.parameter_file_list = self.parameter_file if self.parameter_file else []
        self.connector_data = kwargs.get("connector_data", False)
        self.exclude_directories = [".git"]
        self.template_references = {
            "main_templates" : [],
            "module_templates" : []
        }
        self.outputs = {}
        self.skip_key_to_process = ["compiletime_identity", "depends_on"]
        self.group_count = 0

    def is_template_file(self, file_path):
        """
        check for valid template file for parse terraform template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "tf":
            json_data = hcl_to_json(file_path)
            return True if (json_data and ("resource" in json_data or "module" in json_data)) else False
        elif len(file_path.split(".")) > 0 and file_path.split(".")[-1] == "json":
            json_data = json_from_file(file_path, escape_chars=['$'])
            return True if (json_data and ("resource" in json_data or "module" in json_data)) else False
    
    def is_parameter_file(self, file_path):
        """
        check for valid variable file for parse terraform template
        """
        if len(file_path.split(".")) > 0 and file_path.split(".")[-1] in ["tf", "tfvars"]:
            json_data = hcl_to_json(file_path)
            return True if (json_data and not "resource" in json_data) else False
        elif len(file_path.split(".")) > 1 and [ele for ele in [".tfvars.json", ".tf.json"] if(ele in file_path)]:
            json_data = json_from_file(file_path, escape_chars=['$'])
            return True if (json_data and not "resource" in json_data) else False
        return False

    def process_locals(self, resource):
        """
        return value of the local variable
        """
        status, value = self.parse_field_value(resource, self.locals)
        return status, value

    def process_other(self, resource):
        """
        return default value of the variable if variable is set in terraform files
        """
        main_status = False

        status, value = self.parse_field_value(resource, self.resource)
        main_status = True if status else main_status
        if value is None:
            status, value = self.parse_field_value(resource, self.module_params)
            main_status = True if status else main_status
        if value is None:
            status, value = self.parse_field_value(resource, self.temp_params)
            main_status = True if status else main_status
        return main_status, value

    def process_variable(self, resource):
        """
        return default value of the variable if variable is set in terraform files
        """
        main_status = False
        status, value = self.parse_field_value(resource, self.default_gparams)
        main_status = True if status else main_status
        if value is None:
            status, value = self.parse_field_value(resource, self.gparams)
            main_status = True if status else main_status
        if value is None:
            status, value = self.parse_field_value(resource, self.resource)
            main_status = True if status else main_status
        return main_status, value
    
    def process_data(self, resource):
        """
        return value of the data if the given data is contains in terraform template file
        """
        return self.parse_field_value(resource, self.gdata)
    
    def parse_field_value(self, resource, from_data):
        resource_list = re.compile("\.(?![^[]*\])").split(resource)
        value = copy.deepcopy(from_data)
        is_valid = True
        for resource in resource_list:
            # process variables like this: var.network_http["cidr"]
            pattern = re.compile(r'\[(.*?)\]')
            map_keys = re.findall(pattern, resource)
            if map_keys and len(resource.split("[")) > 1:
                res = resource.split("[")[0]
                if res in value:
                    value = value.get(res)
                elif isinstance(value, list):
                    for val in value:
                        if isinstance(res, dict) and res in val:
                            value = val.get(res)
                else:
                    value = None
                    is_valid = False
                    break
                for key in map_keys:
                    key = self.parse_string(key)
                    if key == "count.index" and isinstance(value, list) and len(value) > self.count:
                        value = value[self.count]
                        continue
                    elif isinstance(value, list):
                        result, res = self.check_numeric_value(key)
                        if result and isinstance(res, int) and len(value) > res:
                            value = value[res]
                            continue
                    elif value is None or not isinstance(value, dict):
                        is_valid = False
                        break

                    if key in value:
                        value = value.get(key)
                    else:
                        value = None
                        is_valid = False
                if value is None:
                    break
                continue
            if isinstance(value, list) and resource == "*" and self.count is not None and self.count < len(value):
                value = value[self.count]
            elif isinstance(value, dict):            
                if resource in value:
                    value = value.get(resource)
                elif resource == "json":
                    pass
                else:
                    value = None
                    is_valid = False
                if value is None:
                    break
            else:
                value = None
                is_valid = False
                break
        
        if is_valid:
            return True, value
        else:
            return False, value
    
    def get_template(self):
        """
        return the template json data
        """
        # used for terraform file remediation
        self.template_references["main_templates"].append({
            "main_file_path" : self.get_ralative_path(self.template_file)
        })

        json_data = None
        if len(self.template_file.split(".")) > 0 and self.template_file.split(".")[-1]=="tf":
            json_data = hcl_to_json(self.template_file)
            self.contentType = 'terraform'
        elif len(self.template_file.split(".")) > 1 and ".tf.json" in self.template_file:
            json_data = json_from_file(self.template_file, escape_chars=['$'])
        return json_data
    
    def get_paramter_json_list(self):
        """
        process parameter files and returns parameters json list
        """
        parameter_json_list = []
        for parameter in self.parameter_file:
            if len(parameter.split(".")) > 0 and parameter.split(".")[-1] in ["tf", "tfvars"]:
                json_data = hcl_to_json(parameter)
                if json_data:
                    parameter_json_list.append({parameter.split(".")[-1] : json_data})
            elif len(parameter.split(".")) > 1 and [ele for ele in [".tfvars.json", ".tf.json"] if(ele in parameter)]:
                json_data = json_from_file(parameter, escape_chars=['$'])
                if json_data:
                    splited_list = parameter.split(".")
                    parameter_json_list.append({'.'.join(splited_list[len(splited_list)-2:]) : json_data})
        return parameter_json_list
    
    def get_ralative_path(self, file_path):
        """
        takes full path of template or parameter file and returns the relative path by removing `temp` directory path
        """
        split_path = file_path.split("/")
        return "/%s" % "/".join(split_path[3:]).replace("//","/")

    def generate_template_json(self):
        """
        generate the template json from template and parameter files
        """
        template_json = self.get_template()
        parameter_jsons = self.get_paramter_json_list()
        gen_template_json = None
        if template_json:
            gen_template_json = copy.deepcopy(template_json)
            for parameter_json in parameter_jsons:
                for file_type, variable_json in parameter_json.items():
                    if file_type in ["tfvars", "tfvars.json"]:
                        for key, value in variable_json.items():
                            if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str):
                                value[0] = self.parse_string(value[0])
                            key = self.parse_string(key)
                            self.gparams[key] = value
                    else:
                        if "variable" in variable_json:
                            for var in variable_json["variable"]:
                                for key, value in var.items():
                                    if "default" in value:
                                        self.gparams[key] = value["default"] 

                    if "locals" in variable_json:
                        var_locals = []
                        for local_var in variable_json["locals"]:
                            local_dic = {}
                            for local_key, local_value in local_var.items():
                                processed_data, processed = self.process_resource(local_value, count=self.count)
                                self.locals[local_key] = processed_data
                                local_dic[local_key] = processed_data
                            var_locals.append(local_dic)
                        variable_json['locals'] = var_locals

            if "variable" in template_json:
                for var in template_json["variable"]:
                    for key, value in var.items():
                        if "default" in value:
                            self.gparams[key] = value["default"]

            if "locals" in template_json:
                locals = []
                for var in template_json["locals"]:
                    local_dic = {}
                    for key, value in var.items():
                        processed_data, processed = self.process_resource(value, count=self.count)
                        self.locals[key] = processed_data
                        local_dic[key] = processed_data
                    locals.append(local_dic)
                gen_template_json['locals'] = locals

            if 'data' in template_json:
                data_resource = {}
                for data_item in template_json['data']:
                    for data_key, data_value in data_item.items():
                        processed_data, processed = self.process_resource(data_value, count=self.count)
                        if isinstance(processed_data, dict):
                            for processed_key, processed_value in processed_data.items():
                                if isinstance(processed_value, dict):
                                    processed_value["compiletime_identity"] = "data.%s.%s" % (data_key, processed_key)
                                if isinstance(processed_value, list):
                                    for resource_property in processed_value:
                                        resource_property["compiletime_identity"] = "data.%s.%s" % (data_key, processed_key)
                                if data_key in self.gdata:
                                    self.gdata[data_key][processed_key] = processed_value
                                    data_resource[data_key][processed_key] = processed_value
                                else:
                                    self.gdata[data_key] = { processed_key : processed_value }
                                    data_resource[data_key] = { processed_key : processed_value }
                gen_template_json['data'] = data_resource
            
            new_resources = {}
            if "module" in template_json:
                for mod in template_json["module"]:
                    for key, value in mod.items():
                        if "source" in value:
                            count_resource, processed_count = self.process_count(value)
                            if processed_count and isinstance(count_resource, list):
                                for value in count_resource:
                                    self.process_module_resource(key, value, new_resources)
                            else:
                                self.process_module_resource(key, value, new_resources)
                            
                if "module" in gen_template_json:
                    del gen_template_json["module"]
            
            self.resource = {}
            resources = []
            if "resource" in new_resources and isinstance(new_resources["resource"], list):
                for resource in new_resources["resource"]:
                    for resource_name, properties in resource.items():
                        processed_resource, processed = self.process_resource(properties, count=self.count)
                        if not self.process_module:
                            if resource_name in self.resource:
                                self.resource[resource_name].append(processed_resource)
                            else:
                                self.resource[resource_name] = [processed_resource]
                        else:
                            self.resource[resource_name] = processed_resource

            if 'resource' in template_json:
                for res in template_json['resource']:
                    for resource_name, properties in res.items():
                        processed_resource, processed = self.process_resource(properties, count=self.count)
                        if not self.process_module:
                            if resource_name in self.resource:
                                self.resource[resource_name].append(processed_resource)
                            else:
                                self.resource[resource_name] = [processed_resource]
                        else:
                            if resource_name in self.resource and isinstance(self.resource[resource_name], dict) and isinstance(processed_resource, dict):
                                self.resource[resource_name].update(processed_resource)
                            else:    
                                self.resource[resource_name] = processed_resource

            if not self.process_module:
                for resource_name, processed_resource_list in self.resource.items():
                    for processed_resource in processed_resource_list:
                        if isinstance(processed_resource, dict):
                            for name, properties in processed_resource.items():
                                if isinstance(properties, list):
                                    for property_obj in properties:
                                        self.resource_types.append(resource_name.lower())
                                        if "compiletime_identity" not in property_obj:
                                            property_obj["compiletime_identity"] = "%s.%s" % (resource_name.lower(), name)
                                        resources.append({
                                            "type" : resource_name,
                                            "name" : name,
                                            "properties" : property_obj
                                        })    
                                else:
                                    self.resource_types.append(resource_name.lower())
                                    if "compiletime_identity" not in properties:
                                        properties["compiletime_identity"] = "%s.%s" % (resource_name.lower(), name)
                                    resources.append({
                                        "type" : resource_name,
                                        "name" : name,
                                        "properties" : properties
                                    })
                    gen_template_json['resources'] = resources

                    if 'resource' in gen_template_json:
                        del gen_template_json['resource']
            else:
                for parameter_json in parameter_jsons:
                    for file_type, variable_json in parameter_json.items():
                        if file_type == "tf" and "output" in variable_json:
                            for output in variable_json["output"]:
                                for key, value in output.items():
                                    if "value" in value:
                                        processed_data, _ = self.process_resource(value["value"], count=self.count)
                                        self.outputs[key] = processed_data
                gen_template_json['resource'] = self.resource
            
        return gen_template_json
    
    def process_module_resource(self, module_key, module_value, new_resources):
        default_gparams = {}
        self.module_params["module"][module_key] = {}
        for k, v in module_value.items():
            if k != "source":
                processed_data, processed = self.process_resource(v, count=self.count)
                default_gparams[k] = processed_data
                self.module_params["module"][module_key][k] = processed_data

        full_path_list = self.template_file.split("/")[:-1]
        template_file_path = ("/".join(full_path_list)).replace("//","/")
        module_parser = ModuleParser(module_value["source"], template_file_path, connector_data=self.connector_data)
        module_file_path = module_parser.process_source()

        if not module_file_path:
            return
        
        logger.info("Finding module : %s", module_file_path)
        if exists_dir(module_file_path):
            list_of_file = os.listdir(module_file_path)

            template_file_path_list = []
            parameter_file_list = []
            for entry in list_of_file:
                if any(exclude_dir in entry for exclude_dir in self.exclude_directories):
                    continue
                new_file_path = ('%s/%s' % (module_file_path, entry)).replace('//', '/')
                self.template_references["module_templates"].append({
                    "main_file_path" : self.get_ralative_path(self.template_file),
                    "module_file_path" : self.get_ralative_path(new_file_path),
                    "module_label" : module_key
                })
                if exists_file(new_file_path):
                    if self.is_template_file(new_file_path):
                        template_file_path_list.append(new_file_path)
                    elif self.is_parameter_file(new_file_path):
                        parameter_file_list.append(new_file_path)
            
            if template_file_path_list and parameter_file_list:
                for template_file_path in template_file_path_list:
                    terraform_template_parser = TerraformTemplateParser(
                        template_file_path,
                        parameter_file=parameter_file_list,
                        **{"default_gparams" : default_gparams, "process_module" : True, "locals" : self.locals })
                    new_template_json = terraform_template_parser.parse()

                    self.template_file_list = self.template_file_list + terraform_template_parser.template_file_list
                    self.parameter_file_list = self.parameter_file_list + terraform_template_parser.parameter_file_list

                    
                    if new_template_json:
                        for resource, resource_item in new_template_json.items():
                            # set parameters from modules files to main resource file
                            if resource == "resource":
                                for resource_key, resource_value in resource_item.items():
                                    for resource_name, resource_properties in resource_value.items():
                                        if isinstance(resource_properties, dict):
                                            # for default_key, default_value in default_gparams.items():
                                                # if default_key not in resource_properties:
                                                #     resource_properties[default_key] = default_value
                                            resource_properties["compiletime_identity"] = "module.%s" % module_key
                                        if isinstance(resource_properties, list):
                                            for resource_property in resource_properties:
                                                # for default_key, default_value in default_gparams.items():
                                                #     if default_key not in resource_property:
                                                #         resource_property[default_key] = default_value
                                                resource_property["compiletime_identity"] = "module.%s" % module_key
                            if resource not in new_resources:
                                new_resources[resource] = [resource_item]
                            else:
                                new_resources[resource].append(resource_item)
        else:
            logger.error("module does not exist : %s ", module_value["source"])
    
    def process_count(self, resource):
        new_resource_list = []
        processed_count = False
        r_count = resource.get("count")
        if r_count:
            count_resource, processed = self.process_resource(r_count, count=self.count)
            if isinstance(count_resource, str):
                result, res = self.check_numeric_value(count_resource)
                if result:
                    count_resource = res
                
            if isinstance(count_resource, int):
                processed_count = True
                for i in range(count_resource):
                    new_resource_dict = {}
                    process_resource = copy.deepcopy(resource)
                    process_resource["count"] = i
                    del process_resource["count"]
                    self.count = i
                    for key, value in process_resource.items():
                        if key in self.skip_key_to_process:
                            new_resource_dict[key] = value
                            continue
                        elif key == "dynamic" and value and isinstance(value, list) and isinstance(value[0], dict):
                            processed_resource, processed = self.process_resource({ "dynamic" : value }, count=i)
                            if processed_resource and isinstance(processed_resource, dict):
                                for res, val in processed_resource.items():
                                    new_resource_dict[res] = val
                        else:
                            processed_resource, processed = self.process_resource(value, count=i)
                            new_resource_dict[key] = processed_resource
                    new_resource_list.append(new_resource_dict)
                self.count = None
        return new_resource_list, processed_count
    
    def check_numeric_value(self, resource):
        """ check that resource is numeric value or not and return the numeric value """
        try:
            resource = int(resource)
            return True, resource
        except ValueError:
            pass

        try:
            resource = float(resource)
            return True, resource
        except ValueError:
            pass

        return False, resource
    
    def check_json_or_list_value(self, resource, count=None):
        """ check that string resource is json or list type or not and return the list or json value """
        json_data = json_from_string(resource.replace("\'","\""))
        if json_data:
            resource, processed = self.process_resource(json_data, count=count)
            return True, resource
        
        json_data = json_from_string(re.sub(r"(?<!\\)\"", "\\\"", resource).replace("\'","\""))
        if json_data:
            resource, processed = self.process_resource(json_data, count=count)
            return True, resource
        
        try:
            if resource.startswith('[') and resource.endswith(']'):
                update_resource, processed = self.process_resource(resource[1:-1], count=count)
                list_data = ast.literal_eval("[" + str(update_resource) + "]")
                resource, processed = self.process_resource(list_data, count=count)
                return True, resource
        except:
            pass

        return False, resource
    
    def parse_string(self, resource):
        if resource.startswith('"') and resource.endswith('"'):
            resource = resource[1:-1]
        elif resource.startswith("'") and resource.endswith("'"):
            resource = resource[1:-1]
        return resource

    def split_parameters(self, value):
        try:
            value = "[%s]" % value
            value = value.replace("'", '"')
            parsed = hcl2.loads('split = %s \n' % value)
            
            params = []
            for split_str in parsed["split"]:
                if split_str != None:
                    split_str = str(split_str)
                    exmatch = re.search(r'^\${.*}$', split_str, re.I)
                    if exmatch:
                        match_values = re.search(r'(?<=\{).*(?=\})', split_str, re.I)
                        if match_values:
                            split_str = match_values.group(0)
                        else:
                            split_str = exmatch.group(0)[2:-1]
                
                params.append(split_str)
            return params 
        except Exception as e:
            logger.debug("Failed to split paramaters")
            logger.debug(traceback.format_exc())
            return []

    def process_expression_parameters(self, param_str, count):
        
        processed_groups = {}
        
        groups = self.find_functions_all(param_str)
        if groups:
            for group in groups:
                if group != param_str:
                    updated_group, processed = self.process_resource(group, count)
                    if processed:
                        self.group_count += 1
                        group_name = "group%s" % str(self.group_count)
                        param_str = param_str.replace(group, group_name)
                        processed_groups[group_name] = str(updated_group)

        groups = re.findall(r'^[(].*[,].*[)]|.* ([(].*[)])', param_str, re.I)
        if groups:
            for group in groups:
                if group != param_str:
                    parameter_str = re.findall("(?<=\().*(?=\))", group)[0]
                    updated_group, p_groups = self.process_expression_parameters(parameter_str, count)

                    processed_groups.update(p_groups)

                    self.group_count += 1
                    group_name = "group%s" % str(self.group_count)
                    param_str = param_str.replace(group, group_name)
                    processed_groups[group_name] = str(updated_group)

        # groups = re.findall(r'(?<=\?)([a-z0-9A-Z._\-\s]*(\?){1}[a-z0-9A-Z._\-\s]*(\:){1}[a-z0-9A-Z._\-\s]*)(?=:)', param_str, re.I)
        groups = re.findall(r'(?<=\?\s)(.*[?].*[:].*)(?=\s:)', param_str, re.I)
        if groups:
            for group in groups:
                if group != param_str:
                    updated_group, processed = self.process_resource(group, count)
                    if processed:
                        self.group_count += 1
                        group_name = "group%s" % str(self.group_count)
                        param_str = param_str.replace(group, group_name)
                        processed_groups[group_name] = str(updated_group)

        return param_str, processed_groups

    def eval_expression(self, resource):
        try:
            response = eval(resource)
            return response, True
        except Exception as e:
            return resource, False
        

    def process_resource(self, resource, count=None, nested_string_params={}):
        """ 
        process the resource json and return the resource with updated values
        """
        processed = True
        new_resource = ""
        if isinstance(resource, list):
            new_resource_list = [] 
            for value in resource:
                processed_resource, processed = self.process_resource(value, count=count)
                if processed and isinstance(value, str) and isinstance(processed_resource, list):
                    process_var = value.split(".") 
                    if len(process_var) > 1:
                        new_resource_list += processed_resource
                        continue
                new_resource_list.append(processed_resource)
            new_resource = new_resource_list
        
        elif isinstance(resource, dict):
            new_resource = {}
            new_resource_list = []
            r_count = resource.get("count")
            if r_count:
                count_resource, processed = self.process_resource(r_count, count=count)
                if isinstance(count_resource, str):
                    result, res = self.check_numeric_value(count_resource)
                    if result:
                        count_resource = res
                    
                if isinstance(count_resource, int):
                    for i in range(count_resource):
                        new_resource_dict = {}
                        process_resource = copy.deepcopy(resource)
                        process_resource["count"] = i
                        del process_resource["count"]
                        self.count = i
                        for key, value in process_resource.items():
                            if key in self.skip_key_to_process:
                                new_resource_dict[key] = value
                                continue
                            elif key == "dynamic" and value and isinstance(value, list) and isinstance(value[0], dict):
                                processed_resource, processed = self.process_resource({ "dynamic" : value }, count=i)
                                if processed_resource and isinstance(processed_resource, dict):
                                    for res, val in processed_resource.items():
                                        new_resource_dict[res] = val
                            else:
                                processed_resource, processed = self.process_resource(value, count=i)
                                new_resource_dict[key] = processed_resource
                        new_resource_list.append(new_resource_dict)
                    self.count = None
                    new_resource = new_resource_list
                else:
                    for key, value in resource.items():
                        if key in self.skip_key_to_process:
                            new_resource[key] = value
                            continue
                        processed_resource, processed = self.process_resource(value, count=count)
                        new_resource[key] = processed_resource
            else:
                for key, values in resource.items():
                    if key in self.skip_key_to_process:
                        new_resource[key] = values
                        continue
                    # if key == "dynamic" and isinstance(value, dict):
                    if key == "dynamic" and values and isinstance(values, list) and isinstance(values[0], dict):
                        for value in values:
                        # value = value[0]
                            loop_values = []
                            for main_key, loop_content in value.items():
                                var = main_key
                                resource_properties = []
                                if isinstance(loop_content, dict):
                                    for loop_content_key, loop_content_value in loop_content.items():
                                        if loop_content_key == "for_each":
                                            loop_values, processed = self.process_resource(loop_content_value, count=count)
                                        if loop_content_key == "iterator":
                                            var, processed = self.process_resource(loop_content_value, count=count)
                                        # if loop_content_key == "content" and isinstance(loop_content_value, dict):
                                        if loop_content_key == "content" and loop_content_value and \
                                            isinstance(loop_content_value, list) and isinstance(loop_content_value[0], dict):
                                            loop_content_value = loop_content_value[0]
                                            if isinstance(loop_values, list):
                                                for loop_value in loop_values:
                                                    resource_property = {}
                                                    for content_key, content_value in loop_content_value.items():
                                                        if isinstance(content_value, str):
                                                            self.temp_params[var] = {
                                                                "value" : loop_value
                                                            }
                                                            # content_value = content_value.replace(var+".value",str(loop_value))
                                                        
                                                        content_value, processed = self.process_resource(content_value, count=count)
                                                        resource_property[content_key] = content_value
                                                        self.temp_params = {}
                                                    resource_properties.append(resource_property)
                                            elif isinstance(loop_values, dict):
                                                for loop_key, loop_value in loop_values.items():
                                                    resource_property = {}
                                                    for content_key, content_value in loop_content_value.items():
                                                        if isinstance(content_value, str):
                                                            self.temp_params[var] = {
                                                                "value" : loop_value,
                                                                "key" : loop_key
                                                            }
                                                            # content_value = content_value.replace(var+".value",str(loop_value))
                                                            # content_value = content_value.replace(var+".key",str(loop_key))
                                                        content_value, processed = self.process_resource(content_value, count=count)
                                                        resource_property[content_key] = content_value
                                                        self.temp_params = {}
                                                    resource_properties.append(resource_property)
                                                    
                                                # temp_params = {}
                                                # temp_params[var] = { "value" : loop_values}                
                                                # resource_property = {}
                                                # for content_key, content_value in loop_content_value.items():
                                                #     if isinstance(content_value, str):
                                                #         self.temp_params = temp_params
                                                #     else:
                                                #         self.temp_params = {}
                                                #         # content_value = content_value.replace(var+".value",str(loop_value))
                                                #         # content_value = content_value.replace(var+".key",str(loop_key))
                                                #     content_value, processed = self.process_resource(content_value, count=count)
                                                #     resource_property[content_key] = content_value
                                                #     self.temp_params = {}
                                                # resource_properties.append(resource_property)
                                if main_key in new_resource:
                                    new_resource[main_key].extend(resource_properties)
                                else:
                                    new_resource[main_key] = resource_properties
                    else:
                        processed_resource, processed = self.process_resource(values, count=count)
                        new_resource[key] = processed_resource
        
        elif isinstance(resource, str):
            # match the substrings for replace the value
            # pattern = re.compile(r'(var\..\w*)')
            # exmatch = re.findall(pattern, resource)
            parsed_string = self.parse_string(resource)

            if re.match(r"^\{.*\}$", parsed_string.strip().replace("\n", "")):
                json_data = json_from_string(re.sub(r"\n", "", parsed_string).replace("\\",""))
                if json_data:
                    parsed_string, processed = self.process_resource(json_data, count=count)
                    return parsed_string, True

            for_loop_expression = r'\[for\s(.*)\sin\s(.*)\s:\s(.*)\]'
            for_loop_parameters = re.search(for_loop_expression, parsed_string, re.I)

            new_resource = copy.deepcopy(parsed_string)
            match_full = re.match(r'^\${([^}$]*)}$', new_resource)
            if match_full:
                matched_str = new_resource[2:-1]
            else:
                expression_parameter = False
                for func in expression_list:
                    m = re.match(func['expression'], new_resource)
                    if m:
                        expression_parameter = True
                    
                all_exmatch = re.findall(r'\${([^}$]*)}', new_resource)
                if all_exmatch and not expression_parameter and not for_loop_parameters:
                    for exmatch in all_exmatch:
                        processed_param, processed = self.process_resource("${" + copy.deepcopy(exmatch).strip() + "}", count=count)
                        parsed_string = parsed_string.replace("${" + exmatch + "}", str(processed_param))
                    new_resource = copy.deepcopy(parsed_string)
                    matched_str = parsed_string
                else:
                    matched_str = parsed_string

            for_loop_parameters = re.search(for_loop_expression, matched_str, re.I)
            if for_loop_parameters:
                for_loop_items = []
                # Process terraform `for-expressions`
                temp_loop_variable = for_loop_parameters.group(1)
                loop_source_list = for_loop_parameters.group(2)
                loop_value = for_loop_parameters.group(3)
                processed_loop_source_list, _ = self.process_resource(loop_source_list, count=count)

                if processed_loop_source_list and isinstance(processed_loop_source_list, list):
                    for item in processed_loop_source_list:
                        new_loop_value = copy.deepcopy(loop_value)
                        new_loop_value_list = re.findall(r"[^\w]"+ temp_loop_variable + "[^\w]", new_loop_value)
                        for match_param in new_loop_value_list:
                            new_match_param = match_param.replace(temp_loop_variable, "'%s'" % str(item))
                            new_loop_value = new_loop_value.replace(match_param, new_match_param)

                        processed_new_loop_value, _ = self.process_resource(new_loop_value, count=count)
                        for_loop_items.append(processed_new_loop_value)
                
                return for_loop_items, True

            exmatch = re.search(r'\${([^}]*)}', matched_str, re.I)
            if exmatch:
                match_values = re.search(r'(?<=\{).*(?=\})', matched_str, re.I)
                if match_values:
                    matched_str = match_values.group(0)
                else:
                    matched_str = exmatch.group(0)[2:-1]
            matched_str = matched_str.strip()
            matched_str = self.parse_string(matched_str)

            # if not re.match(r'^([.a-zA-Z]+[(].*[,].*[)])$', matched_str) and \
            #     not re.match(r'^[(].*[,].*[)]|.* ([(].*[)])', matched_str):
            #     matched_str = self.process_expression_parameters(matched_str, count)
                
            result, res = self.check_numeric_value(matched_str)
            if result:
                new_resource = res
                return new_resource, processed

            result, res = self.check_json_or_list_value(matched_str, count=count)
            if result:
                new_resource = res
                return new_resource, processed

            for func in default_functions:
                m = re.match(func['expression'], matched_str)
                if not m:
                    continue

                parameter_str = re.findall("(?<=\().*(?=\))", m.group(0))[0]
                parameters = []
                process = True
                    
                found_parameters = self.split_parameters(parameter_str.strip())

                for param in found_parameters:
                # for param in re.findall("(?:[^,()]|\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\))+", parameter_str.strip()):
                # for param in parameter_str.strip().split(","):
                    param_exmatch = re.search(r'(^[\'|\"]\${([^}]*)}[\'|\"]$)|(^\${([^}]*)}$)', param.strip(), re.I)
                    if param_exmatch:
                        match_values = re.search(r'(?<=\{).*(?=\})', param.strip(), re.I)
                        if match_values:
                            param = match_values.group(0)
                    if param in nested_string_params:
                        param = str(nested_string_params[param])

                    processed_param, process_status = self.process_resource("${" + param.strip() + "}", count)
                    processed = processed and process_status
                    if (isinstance(processed_param, str) and re.search(r'\${([^}]*)}', processed_param, re.I)):
                        process = False
                        parameters.append(param.strip())
                    # Check only for None return
                    elif processed_param == None and re.match(".*(\.\*\.).*", param.strip()):
                        process = False
                        parameters.append(param.strip())
                    elif isinstance(processed_param, str) and re.findall(r'([.a-zA-Z]+)[(].*[,].*[)]', processed_param.strip(), re.I):
                        process = False
                        parameters.append(param.strip())
                    else:
                        parameters.append(processed_param)

                args = inspect.getargspec(func['method']).args
                varargs = inspect.getargspec(func['method']).varargs
                keywords = inspect.getargspec(func['method']).keywords
                defaults = inspect.getargspec(func['method']).defaults

                if process and ((len(args) == len(parameters)) or \
                    (defaults and len(parameters) <= len(args) and len(parameters) >= (len(args) - len(defaults))) or \
                    varargs or keywords):
                    try:
                        new_resource = func['method'](*parameters)
                    except Exception as e:
                        processed = False
                        logger.debug("Failed to process %s : %s", new_resource, str(e))
                else:
                    processed = False
                    parameters = [str(ele) for ele in parameters]
                    new_resource = func['method'].__name__ + "(" + ",".join(parameters) + ")"
                break 
            else:
                for func in expression_list:
                    m = re.match(func['expression'], matched_str)
                    if not m:
                        continue

                    parameter_str = m.group(0)
                    parameter_str, processed_groups = self.process_expression_parameters(parameter_str, count)
                    
                    string_params = {}
                    groups = re.findall(r'\".*?\"', parameter_str, re.I)
                    if groups:
                        i = 0
                        for group in groups:
                            if group != parameter_str:
                                updated_group, _ = self.process_resource(groups[i], count)
                                string_params["group%s" % (str(i))] = updated_group
                                parameter_str = parameter_str.replace(group, "group%s" % (str(i)))
                                i+=1
                    
                    # params = re.findall(r"[a-zA-Z0-9.()\[\]_*\"]+|(?:(?![a-zA-Z0-9.()\[\]_*\"]).)+", parameter_str)
                    params = re.findall(r"[a-zA-Z0-9.()\[\],-_*\"\'\{\$\}]+|(?:(?![ a-zA-Z0-9.()\[\]_*\"\'\{\$\}]).)+", parameter_str)

                    if params and len(params) > 1:
                        new_parameter_list = []
                        process_function = True
                        for param in params:
                            if param in string_params:
                                param = str(string_params[param])
                            if param in nested_string_params:
                                param = str(nested_string_params[param])
                            if param in processed_groups:
                                param = str(processed_groups[param])

                            processed_param, processed = self.process_resource("${" + param.strip() + "}", count=count, nested_string_params=string_params)
                            if isinstance(processed_param, str) and (re.findall(r".*\(.*\)", processed_param) or re.findall(r"\${([^}]*)}", processed_param)):
                                process_function = False # parameter processing failed
                                new_parameter_list.append("\"" + param + "\"")
                            elif isinstance(processed_param, str) and re.findall(r"[a-zA-Z-_]", processed_param) and processed_param not in self.replace_value_str:
                                new_parameter_list.append("\"" + processed_param + "\"")
                            elif isinstance(processed_param, str) and len(processed_param) == 0:
                                new_parameter_list.append('""')
                            elif processed_param is None and len(param.strip().split(".")) > 1 and not processed:
                                process_function = False # variable value not set in vars.tf file
                                new_parameter_list.append("\"" + param + "\"")
                            else:
                                new_parameter_list.append(str(processed_param))

                        if process_function:
                            try:
                                new_resource, processed = func['method'](" ".join(new_parameter_list))
                            except Exception as e:
                                processed = False
                                logger.debug("Failed to process %s : %s", new_resource, str(e))
                        else:
                            new_resource = matched_str
                    break
                else:
                    splited_list = matched_str.split(".") 
                    if len(splited_list) > 1:
                        if splited_list[0] in self.schema_filter:
                            result, new_value = self.schema_filter[splited_list[0]](".".join(splited_list[1:]))
                            if result:
                                new_resource = new_value
                            else:
                                processed = False
                        else:
                            if matched_str == "count.index" and count is not None:
                                new_resource = count
                            elif re.search(r'[A-Za-z]+', splited_list[0]):
                                result, new_value = self.schema_filter["other"](".".join(splited_list))
                                if result:
                                    new_resource = new_value
                            else:
                                new_resource = ".".join(splited_list)
                    else:
                        new_resource = matched_str
        else:
            new_resource = resource
        
        if isinstance(new_resource, str) and new_resource.strip() in self.replace_values:
            new_resource = self.replace_values[new_resource.strip()]
            
        if isinstance(new_resource, str) and "count.index" in new_resource and isinstance(self.count, int):
            new_resource = new_resource.replace("count.index", str(self.count))
            match_full = re.findall(r'^\${(?<=\{)(.*)(?=\})}', new_resource)
            if match_full:
                new_resource = new_resource[2:-1]

            res, result = self.eval_expression(new_resource)
            if result:
                processed = True
                new_resource = res

        return new_resource, processed
