def camel_to_snake(camel_case_string):
    snake_case_string = ""
    for i in range(len(camel_case_string)):
        if camel_case_string[i].isupper() and i > 0:
            snake_case_string += "_" + camel_case_string[i].lower()
        else:
            snake_case_string += camel_case_string[i].lower()
    return snake_case_string