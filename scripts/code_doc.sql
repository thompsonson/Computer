SELECT
    git_projects.origin_url AS git_project_url,
    source_files.file_path AS source_path,
    code_classes.name AS class_name,
    functions.name AS method_name,
    functions.docstring AS method_docstring
FROM
    code_classes
LEFT JOIN
    functions ON code_classes.id = functions.code_class_id
LEFT JOIN
    source_files ON functions.source_file_id = source_files.id
LEFT JOIN
    python_modules ON source_files.module_id = python_modules.id
LEFT JOIN
    git_projects ON python_modules.git_project_id = git_projects.id
--WHERE
--    functions.docstring IS NOT NULL
ORDER BY 
    git_project_url, source_path, class_name, method_name
;


SELECT
    git_projects.origin_url AS git_project_url,
    source_files.file_path AS source_path,
    code_classes.name AS class_name,
    functions.name AS method_name,
    functions.docstring AS method_docstring,
    GROUP_CONCAT(arguments.name) AS argument_names
FROM
    code_classes
LEFT JOIN
    functions ON code_classes.id = functions.code_class_id
LEFT JOIN
    source_files ON functions.source_file_id = source_files.id
LEFT JOIN
    python_modules ON source_files.module_id = python_modules.id
LEFT JOIN
    git_projects ON python_modules.git_project_id = git_projects.id
LEFT JOIN
    arguments ON functions.id = arguments.function_id
--WHERE
--    functions.docstring IS NOT NULL
GROUP BY
    git_project_url, source_path, class_name, method_name, method_docstring
ORDER BY 
    git_project_url, source_path, class_name, method_name;


SELECT
    git_projects.origin_url AS git_project_url,
    source_files.file_path AS source_path,
    code_classes.name AS class_name,
    functions.name AS method_name,
    functions.docstring AS method_docstring,
    GROUP_CONCAT(arguments.name || ':' || arguments.arg_type, char(10)) AS arguments_with_types
FROM
    code_classes
LEFT JOIN
    functions ON code_classes.id = functions.code_class_id
LEFT JOIN
    source_files ON functions.source_file_id = source_files.id
LEFT JOIN
    python_modules ON source_files.module_id = python_modules.id
LEFT JOIN
    git_projects ON python_modules.git_project_id = git_projects.id
LEFT JOIN
    arguments ON functions.id = arguments.function_id
--WHERE
--    functions.docstring IS NOT NULL
GROUP BY
    git_project_url, source_path, class_name, method_name, method_docstring
ORDER BY 
    git_project_url, source_path, class_name, method_name;


SELECT
    git_projects.origin_url AS git_project_url,
    source_files.file_path AS source_path,
    code_classes.name AS class_name,
    functions.name AS method_name,
    functions.docstring AS method_docstring,
    GROUP_CONCAT(arguments.name || ':' || arguments.arg_type, char(10)) AS arguments_with_types,
    GROUP_CONCAT(imports.import_name, char(10)) AS imports
FROM
    code_classes
LEFT JOIN
    functions ON code_classes.id = functions.code_class_id
LEFT JOIN
    source_files ON functions.source_file_id = source_files.id
LEFT JOIN
    python_modules ON source_files.module_id = python_modules.id
LEFT JOIN
    git_projects ON python_modules.git_project_id = git_projects.id
LEFT JOIN
    arguments ON functions.id = arguments.function_id
LEFT JOIN
    imports ON source_files.id = imports.source_file_id
--WHERE
--    functions.docstring IS NOT NULL
GROUP BY
    git_project_url, source_path, class_name, method_name, method_docstring
ORDER BY 
    git_project_url, source_path, class_name, method_name;


SELECT
    git_projects.origin_url AS git_project_url,
    source_files.file_path AS source_path,
    code_classes.name AS class_name,
    functions.name AS method_name,
    functions.docstring AS method_docstring,
    arg_subquery.arguments_with_types,
    GROUP_CONCAT(imports.import_name, char(10)) AS imports
FROM
    code_classes
LEFT JOIN
    functions ON code_classes.id = functions.code_class_id
LEFT JOIN
    source_files ON functions.source_file_id = source_files.id
LEFT JOIN
    python_modules ON source_files.module_id = python_modules.id
LEFT JOIN
    git_projects ON python_modules.git_project_id = git_projects.id
LEFT JOIN
    imports ON source_files.id = imports.source_file_id
LEFT JOIN
    (SELECT
        function_id,
        GROUP_CONCAT(name || ':' || arg_type, char(10)) AS arguments_with_types
     FROM
        arguments
     GROUP BY
        function_id
    ) AS arg_subquery ON functions.id = arg_subquery.function_id
--WHERE
--    functions.docstring IS NOT NULL
GROUP BY
    git_project_url, source_path, class_name, method_name, method_docstring, arg_subquery.arguments_with_types
ORDER BY 
    git_project_url, source_path, class_name, method_name;
