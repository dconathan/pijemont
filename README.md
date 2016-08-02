## Pijemont

Pijemont is a system for generating an HTML form and markdown
documentation from a JSON dictionary specifying the desired arguments.

## Generating a form:

The Pijemont constructor is:

`Pijemont(container_form, api_dict, name, target, submit_callback, function_name)`

* `container_form` is an empty form Element object on the page that will be populated with the form contents
* ` api_dict` is either the actual API dictionary or else a url that will provide this dictionary in response to a GET request
* `name` is any identifier for the form, and should be unique among all Pijemont instances on the page
* `target` is the url to which the form data should be POSTed
* `submit_callback` is a function that will be passed the response data of the submit POST request
* `function_name` is the name of the API function from the provided API that should be used to generate the form

So, for example: 

```
<form enctype="multipart/form-data" id="demo"></form>
<script>
  new Pijemont(document.getElementById("demo"), "/api", "example_form", "/submit_url", function(data){console.log(data);}, "function_name");
</script>
```

will make a GET request to /api for the API dictionary, will place it into the empty form object supplied in the first argument.

Of course, one can replace "/api" with an actual dictionary and generate the form that way.

## Generating documentation

To generate Markdown documentation, simply run:

```
python2 doc.py http://url_of_api_dict
```

and this will output Markdown documentation to stdout.  Note that this script assumes Python 2.7.

## API dictionary format:

The API dictionary is assumed to have its keys being the names of the
various API functions, and values being "type specification"
dictionaries, which we will define now.

A **type specification** in Pijemont is a dictionary, which may look
slightly different depending on the type of argument desired.  It may
contain the following keys:

* `type`: This key is required.  Its value is a string that specifies
  what type of object the argument is.  It can be any of those types
  listed below.

* `description`: A string that describes what the argument is.  Used
  for documentation generation and annotating the form.  This key is
  optional.

* `optional`: This is either `true` or `false` (default is `false`),
  and indicates whether this argument may be omitted

* `default`: This is the value that will be used for the argument if
  it is not supplied (even if it is optional, so having both
  `optional: true` and a `default` value is redundant).

* `values`: If the type is a container for other types (e.g. a list or
  dictionary), then this will be a further type specification of the
  contained values.  If the type is a non-container (such as a string
  or number), then

These behave in
type-specific ways, and we will go through their behaviour in each
case now:

### `number | num | float`

* `values`: May be a list of lists of conditions, such as `` that the numbers must satisfy, such as `[">= 2", "< 3", "== 4"]`
* `default`: A default value for the argument that will pre-populate the form object.  May be omitted.

The form input for this argument will be a numeric input text field.

### `string | str`

* `values`: May be absent or may be a list of strings.  
* `default`: A default string value for the argument that will pre-populate the form object.  May be omitted.

If the `values` key is absent, arbitrary strings are allowed and the
corresponding form input will be a text field.  If `values` is a list
of strings, then the input will be a select with each of the list
items as options.

### `boolean | bool`

* `values`: Should be omitted.
* `default`: A default string value for the argument that will pre-populate the form object.  May be omitted.

If the `values` key is absent, arbitrary strings are allowed and the
corresponding form input will be a text field.  If `values` is a list
of strings, then the input will be a select with each of the list
items as options.

### `multiline`

* `values`: Should be omitted.  
* `default`: A default string value for the argument that will pre-populate the form object.  May be omitted.

The form input for this argument will be a textarea.

### `list`

* `values`: Should be a type specifier dictionary describing the type of each list element.  
* `default`: A list of objects that are valid defaults for the type of the list element.  May be omitted.

This will generate the appropriate form for the given type specifier
dictionary and will allow the user to add or remove these objects from
the list at will.

### `dict`

* `values`: Should be a dictionary whose keys are strings and whose values are type specifier dictionaries.  
* `default`: A dictionary of objects whose keys are a subset of the keys in `values` and whose values are valid default values for the corresponding type specifiers.  May be omitted.

This will generate, for each key, the appropriate form for the
corresponding type specifier dictionary.

### `oneof`

* `values`: Should be a dictionary whose keys are strings and whose values are type specifier dictionaries.  
* `default`: A dictionary of objects whose keys are a subset of the keys in `values` and whose values are valid default values for the corresponding type specifiers.  May be omitted.

This will generate, for each key, the appropriate form for the
corresponding type specifier dictionary, and a radio button allowing
the user to select which single one of the inputs they wish to
provide.

