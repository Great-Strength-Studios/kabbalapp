import yaml

with open('app/app.yml' , 'r') as stream:
    data = yaml.safe_load(stream)

models = data['domain']['models']

for model_name, model in models.items():
    methods = model.get('methods', [])
    methods_dict = {}
    for method in methods:
        methods_dict[method['name']] = method
    model['methods'] = methods_dict

with open('app/app.yml' , 'w') as stream:
    yaml.safe_dump(data, stream, default_flow_style=False)