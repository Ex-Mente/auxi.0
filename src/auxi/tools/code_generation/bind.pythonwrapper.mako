## Helper Functions
<%!
def is_ComplexClass(p, classes, namespace_name):
    isComplexClass = False
    for c in classes:
      if p.type == c.name:
	return True
    for i in c.additional_includes:
      namespaceless_type = p.type.split("::")[-1:][0]
      if i in [p.type, namespaceless_type]:
	return True
    return isComplexClass
def is_Enum(p, enums):
    isEnum = False
    for e in enums:
      if p.type == e.name + "::" + e.name:
    	isEnum = True
    	break
    return isEnum
def getPythonFriendlyName(name):
    if name == "yield": return "yieldAmount"
    return name
# Introspection on types
def isTypeList(type):
    if type[:12] == "std::vector<" and type[-1] not in ["&", "*"]:
        return True
    return False
def isTypeMap(type):
    if type[:9] == "std::map<" and type[-1] not in ["&", "*"]:
        return True
    return False
def shouldWrapFunction(f):
  if f.private:
    return False
  if isTypeList(f.returnType) or isTypeMap(f.returnType):
    return True
  for p in f.params:
    if isTypeList(p[1]) or isTypeMap(p[1]):
        return True
  return False
%>
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
% for c in classes:
% for a_i in c.additional_includes:
% if a_i[0] == "<":
#include ${a_i}
% else:
#include "${a_i}.h"
% endif
% endfor
% endfor
#include "${filename}.h"

using namespace boost::python;
using namespace ${namespace_name};

// Converts a C++ vector to a python list
template <class T>
boost::python::list to_python_list(std::vector<T> vector) {
    typename std::vector<T>::iterator iter;
    boost::python::list list;
    for (iter = vector.begin(); iter != vector.end(); ++iter) {
        list.append(*iter);
    }
    return list;
}

<%
export_func_name = "export_"
export_func_name += namespace_name.replace("::", "_") + "_" + filename
%>
% for c in classes:
    % if c.isNamespace == 'true':
using namespace ${namespace_name}::${c.name[:1].lower() + c.name[1:]};
    % endif
############# Function overloads #####################
% for f in c.functions:
    % if f.private == "true":
<% continue %>
    % endif
<%
  param_count = 0
  param_default_count = 0
  for p in f.params:
    param_count = param_count + 1
    if p[2] is not None:
        param_default_count = param_default_count + 1
%>
% if param_default_count > 0:
% if c.isNamespace == 'true':
BOOST_PYTHON_FUNCTION_OVERLOADS(${c.name}${f.name}, ${f.name}, ${param_count - param_default_count}, ${param_count})
% else:
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(${c.name}${f.name}, ${f.name}, ${param_count - param_default_count}, ${param_count})
% endif
% endif
% endfor
######################################################
    % if c.isNamespace == 'true':
##/////////////////// NAMESPACE ${c.name} ///////////////////
% for f in c.functions:
% if shouldWrapFunction(f):
    <%
        if isTypeList(f.returnType):
            returnType = "list"
            returnStatement = "return to_python_list(result);"
        elif isTypeMap(f.returnType):
            returnType = "dict"
            returnStatement = "result_list = list();\n\t\tfor(auto r: result) result_list.append(r);\n\t\treturn result_list;"
        else:
            returnType = f.returnType
            returnStatement = "return result;"
        params = ""
        param_prep = ""
        params_cpp = ""
        for p in f.params:
            if isTypeList(p[1]):
                item_type = p[1][p[1].index('<')+1:p[1].rindex('>')]
                param_prep += "\n\t{ptype} {pname}_prepped;\n\tfor(int i=0; i<len({pname}); ++i) {pname}_prepped.push_back(extract<{item_type}>({pname}[i]));\n\t\t".format(pname=p[0], ptype=p[1], item_type=item_type)
                params_cpp += p[0] + "_prepped, "
                params += "list " + p[0] + ", "
            elif isTypeMap(p[1]):
                map_types = p[1][p[1].index('<')+1:p[1].rindex('>')].split(',')
                param_prep += "\n\tlist keys = {pname}.keys();\n\t{ptype} {pname}_prepped;\n\tfor(int i=0; i<len(keys); ++i) {{\n\t\tauto curObj = {pname}[keys[i]];\n\t\tif(curObj) {pname}_prepped[extract<{map_type1}>(keys[i])] = extract<{map_type2}>({pname}[keys[i]]);\n\t}}".format(pname=p[0], ptype=p[1], map_type1=map_types[0], map_type2=map_types[1])
                params_cpp += p[0] + "_prepped, "
                params += "dict " + p[0] + ", "
            else:
                params_cpp += p[0] + ", "
                params += p[1] + " " + p[0] + ", "
        if params_cpp[-2] == ',':
            params_cpp = params_cpp[:-2]
            params = params[:-2]
    %>
${returnType} ${f.name}Wrapper(${params})
{
    ${param_prep}
    auto result = ${f.name}(${params_cpp});
    ${returnStatement}
}
    % endif
% endfor
<% continue %>
    % endif
struct ${c.name}Wrapper : ${c.name}, wrapper<${c.name}>
{
  % for f in c.functions:
    % if f.private == "true":
<% continue %>
    % elif f.virtual in ["required","true"]:
    <%
      func_call_params = ""
      func_signature = "static " + f.returnType + " " + f.name + "("
      default_func_signature = f.returnType + " default_" + f.name + "("
      func_signature_rest = ""
      if f.virtual in ["required","true"]:
        if len(f.params) > 0:
          func_call_params = f.params[0][0]
          func_signature_rest = f.params[0][1] + " " + f.params[0][0]
          for pm in f.params[1:]:
            func_call_params = func_call_params + ", " + pm[0]
            func_signature_rest = func_signature_rest + ", " + pm[1] + " " + pm[0]
            if pm[2] is not None:
              func_signature_rest = func_signature_rest + " = " + pm[2]
      func_signature_rest = func_signature_rest + ")"
      func_signature = func_signature + func_signature_rest
      default_func_signature = default_func_signature + func_signature_rest
    %>
        % if f.virtual == "true":
    ${func_signature}
    {
        if (override ${f.name} = this->get_override("${f.name}"))
            % if f.returnType != "void":
            return ${f.name}(${func_call_params});
        return ${c.name}::${f.name}(${func_call_params});
            %else:
            ${f.name}(${func_call_params});
        ${c.name}::${f.name}(${func_call_params});
            % endif
    }
    ${default_func_signature} { return this->${c.name}::${f.name}(${func_call_params}); }
        % elif f.virtual == "required":
    ${func_signature} { return ${f.returnType}(this->get_override("${f.name}")(${func_call_params})); }
        % endif
    % elif shouldWrapFunction(f):
    <%
        if f.custom_constructor == "true":
            returnType = c.name + "*"
            returnStatement = "return result;"
            c.custom_constructor = True
        elif isTypeList(f.returnType):
            returnType = "list"
            returnStatement = "return to_python_list(result);"
        elif isTypeMap(f.returnType):
            returnType = "dict"
            returnStatement = "result_list = list();\n\t\tfor(auto r: result) result_list.append(r);\n\t\treturn result_list;"
        else:
            returnType = f.returnType
            if returnType == "void":
                returnStatement = ""
            else:
                returnStatement = "return result;"
        params = ""
        param_prep = ""
        params_cpp = ""
        for p in f.params:
            if isTypeList(p[1]):
                item_type = p[1][p[1].index('<')+1:p[1].rindex('>')]
                param_prep += "\n\t\t{ptype} {pname}_prepped;\n\t\tfor(int i=0; i<len({pname}); ++i) {pname}_prepped.push_back(extract<{item_type}>({pname}[i]));\n\t\t\t".format(pname=p[0], ptype=p[1], item_type=item_type)
                params_cpp += p[0] + "_prepped, "
                params += "list " + p[0] + ", "
            elif isTypeMap(p[1]):
                map_types = p[1][p[1].index('<')+1:p[1].rindex('>')].split(',')
                param_prep += "\n\t\tlist keys = {pname}.keys();\n\t\t{ptype} {pname}_prepped;\n\t\tfor(int i=0; i<len(keys); ++i) {{\n\t\t\tauto curObj = {pname}[keys[i]];\n\t\t\tif(curObj) {pname}_prepped[extract<{map_type1}>(keys[i])] = extract<{map_type2}>({pname}[keys[i]]);\n\t\t}}".format(pname=p[0], ptype=p[1], map_type1=map_types[0], map_type2=map_types[1])
                params_cpp += p[0] + "_prepped, "
                params += "dict " + p[0] + ", "
            else:
                params_cpp += p[0] + ", "
                params += p[1] + " " + p[0] + ", "
        if params_cpp != "" and params_cpp[-2] == ',':
            params_cpp = params_cpp[:-2]
            params = params[:-2]
    %>
    % if f.custom_constructor == "true":
    static ${returnType} initWrapper(${params})
    % elif params != "":
    static ${returnType} ${f.name}Wrapper(${c.name + " self, " + params})
    % else:
    static ${returnType} ${f.name}Wrapper(${c.name + " self"})
    % endif
    {
        ${param_prep}
        % if f.custom_constructor == "true":
        auto result = new ${f.name}(${params_cpp});
        % else:
        auto result = self.${f.name}(${params_cpp});
        % endif
        ${returnStatement}
    }
    % endif
  % endfor
};
% endfor

void ${export_func_name}()
{
  // Python C++ mappings
% for e in enums:
  enum_<${namespace_name}::${e.name}::${e.name}>("${e.name}", "${e.doc}")
  % for v in e.values:
      .value("${v}", ${e.name}::${v})
  % endfor
      ;
% endfor


% for c in classes:
    % if c.isNamespace == 'true':
    using namespace ${namespace_name}::${c.name[:1].lower() + c.name[1:]};
/////////////////// NAMESPACE ${c.name} ///////////////////
% for f in c.functions:
    <%
    if shouldWrapFunction(f):
        func_name = f.name + "Wrapper"
    else:
        func_name = f.name
    doc = f.doc
    param_args = "args("
    p_default_count = 0
    func_end_char = ""
    for p in f.params:
        if p[2] is not None:
            p_default_count = p_default_count + 1
        param_args += "\"" + p[0] + "\", "
    if p_default_count > 0:
        param_args = c.name + f.name + "(" + param_args
        func_end_char = ")"
    if f.doc is None: doc = "\"\""
    else:
        doc = "\"" + f.doc.replace("\"","\\\"")  + "\\n\"\n\"\\n\"\n"
        for p in f.params:
            doc += "\":param " + p[0] + ": " + p[3].replace("\"","\\\"") + "\\n\"\n"
        if f.doc_return is not None:
            doc += "\"\\n\"\n\":return: " + f.doc_return.replace("\"","\\\"")  + "\""
        if param_args != "args(":
            doc = param_args[:-2] + "), " + doc
    if f.forceCaps == "true":
        py_func_name = f.name[0].upper() + f.name[1:]
    else :
        py_func_name = f.name[0].lower() + f.name[1:]
    %>
      % if f.private != "true" and f.name not in [c.constructor_init_function,c.destructor_clean_function]:
        % if f.returnType[-1:] == "*":
          % if f.virtual == "required":
    //def("${py_func_name}", pure_virtual(make_function(${func_name}, return_internal_reference<1>())), ${doc})${func_end_char};
    def("${py_func_name}", make_function(${func_name}, return_internal_reference<1>()), ${doc})${func_end_char};
          % elif f.virtual == "true":
    //def("${py_func_name}", make_function(${func_name}, return_internal_reference<1>()), make_function(${c.name}Wrapper::default_${f.name}, return_internal_reference<1>()), "${doc}")${func_end_char};
    def("${py_func_name}", make_function(${func_name}, return_internal_reference<1>()), ${doc})${func_end_char};
          % else:
    def("${py_func_name}", make_function(${func_name}, return_internal_reference<1>()), ${doc})${func_end_char};
          % endif
        % elif f.virtual == "required":
    //def("${py_func_name}", pure_virtual(${func_name}), ${doc})${func_end_char};
    def("${py_func_name}", ${func_name}, ${doc})${func_end_char};
        % elif f.virtual == "true":
    //def("${py_func_name}", ${func_name}, ${c.name}Wrapper::default_${f.name}, ${doc})${func_end_char};
    def("${py_func_name}", ${func_name}, ${doc})${func_end_char};
        % else:
    def("${py_func_name}", ${func_name}, ${doc})${func_end_char};
    % endif
      % endif
    % endfor
    % for p in c.properties:
    % if p.private == "true" or (p.set == "false" and p.get == "false"):
<% continue %>
    % endif
<%
    if p.doc is None: prop_doc = ""
    else: prop_doc = p.doc
    if p.forceCaps == "true":
        py_prop_name = getPythonFriendlyName(p.name[0].upper() + p.name[1:])
    else :
        py_prop_name = getPythonFriendlyName(p.name[0].lower() + p.name[1:])
%>
% if isTypeMap(p.type):
    class_<std::map<${p.listItemType}>>("${p.name}Dictionary").def(map_indexing_suite<std::map<${p.listItemType}>>());
% elif isTypeList(p.type):
    class_<std::vector<${p.listItemType}>>("${p.name}List").def(vector_indexing_suite<std::vector<${p.listItemType}>>());
% endif
    scope().attr("${py_prop_name}") = object(m_${p.namelower});
    % endfor
////////////////////////////////////////////////////
<% continue %>
    % endif
<%
    if c.doc is None: class_doc = "\"\""
    else: class_doc = c.doc
    if c.custom_constructor:
        init_statement = "no_init"
        init_def = ".def(\"__init__\", make_constructor(&" + c.name + "Wrapper::initWrapper))"
    else:
        init_statement = "init<>()"
        if c.baseClassName != "Object":
            init_def = ".def(init<std::string, std::string>())"
        else:
            init_def = ""
%>
    % if c.abstract == "true":
    class_<${c.name}Wrapper, ${c.name}*, bases<${c.baseClassName}>, boost::noncopyable>("${c.name}", "${class_doc}", no_init)
    % else:
    class_<${c.name}Wrapper, ${c.name}*, bases<${c.baseClassName}>>("${c.name}", "${class_doc}", ${init_statement})
    % if init_def != "":
	${init_def}
    % endif
    % endif
	.def(self == self)
    % for f in c.functions:
    <%
    if shouldWrapFunction(f):
        func_name = c.name + "Wrapper::" + f.name + "Wrapper"
    else:
        func_name = c.name + "::" + f.name
    # Documentation
    doc = f.doc
    param_args = "args("
    p_default_count = 0
    func_end_char = ""
    for p in f.params:
        if p[2] is not None:
            p_default_count = p_default_count + 1
        param_args += "\"" + p[0] + "\", "
    if p_default_count > 0:
        param_args = c.name + f.name + "(" + param_args
        func_end_char = ")"
    if f.doc is None: doc = "\"\""
    else:
        doc = "\"" + f.doc.replace("\"","\\\"")  + "\\n\"\n\"\\n\"\n"
        for p in f.params:
            doc += "\":param " + p[0] + ": " + p[3].replace("\"","\\\"") + "\\n\"\n"
        if f.doc_return is not None:
            doc += "\"\\n\"\n\":return: " + f.doc_return.replace("\"","\\\"")  + "\""
        if param_args != "args(":
            doc = param_args[:-2] + "), " + doc
    # py functiona name
    if f.forceCaps == "true":
        py_func_name = f.name[0].upper() + f.name[1:]
    else :
        py_func_name = f.name[0].lower() + f.name[1:]
    %>
      % if f.private != "true" and f.name not in [c.constructor_init_function,c.destructor_clean_function, c.name]:
        % if f.returnType[-1:] == "*":
          % if f.virtual == "required":
	//.def("${py_func_name}", pure_virtual(make_function(&${func_name}, return_internal_reference<1>())), ${doc})${func_end_char}
    .def("${py_func_name}", make_function(&${func_name}, return_internal_reference<1>()), ${doc})${func_end_char}
          % elif f.virtual == "true":
    //.def("${py_func_name}", make_function(&${func_name}, return_internal_reference<1>()), make_function(&${c.name}Wrapper::default_${f.name}, return_internal_reference<1>()), ${doc})${func_end_char}
    .def("${py_func_name}", make_function(&${func_name}, return_internal_reference<1>()), ${doc})${func_end_char}
          % else:
    .def("${py_func_name}", make_function(&${func_name}, return_internal_reference<1>()), ${doc})${func_end_char}
          % endif
        % elif f.virtual == "required":
    //.def("${py_func_name}", pure_virtual(&${func_name}), ${doc})${func_end_char}
    .def("${py_func_name}", &${func_name}, ${doc})${func_end_char}
        % elif f.virtual == "true":
    //.def("${py_func_name}", &${func_name}, &${c.name}Wrapper::default_${f.name}, ${doc})${func_end_char}
    .def("${py_func_name}", &${func_name}, ${doc})${func_end_char}
        % else:
	.def("${py_func_name}", &${func_name}, ${doc})${func_end_char}
	% endif
      % endif
    % endfor
    % for p in c.properties:
	% if p.private == "true" or (p.set == "false" and p.get == "false"):
<% continue %>
	% endif
<%
    if p.doc is None:
        prop_doc = "\"\""
    else:
        prop_doc = p.doc.replace('"','\\"')
    if p.forceCaps == "true":
        py_prop_name = getPythonFriendlyName(p.name[0].upper() + p.name[1:])
    else :
        py_prop_name = getPythonFriendlyName(p.name[0].lower() + p.name[1:])
%>
	% if p.isList:
	.add_property("${py_prop_name}", make_function(&${c.name}::Get${p.name}, return_internal_reference<1>()), "${prop_doc}")
	% elif is_ComplexClass(p, classes, namespace_name) or p.type[-1:] == "*":
	  % if p.set == "false":
	.add_property("${py_prop_name}", make_function(&${c.name}::Get${p.name}, return_internal_reference<>()), "${prop_doc}")
	  % elif not is_ComplexClass(p, classes, namespace_name):
	.add_property("${py_prop_name}", make_function(&${c.name}::Get${p.name}, return_internal_reference<>()), &${c.name}::Set${p.name}, "${prop_doc}")
	  % else:
	.add_property("${py_prop_name}", make_function(&${c.name}::Get${p.name}, return_internal_reference<>()), &${c.name}::Set${p.name}, "${prop_doc}")
	  % endif
	% else:
	  % if p.set == "false":
	.add_property("${py_prop_name}", &${c.name}::Get${p.name}, "${prop_doc}")
	  % else:
	.add_property("${py_prop_name}", &${c.name}::Get${p.name}, &${c.name}::Set${p.name}, "${prop_doc}")
	  % endif
        % endif
    % endfor
    ;
% endfor

% for c in classes:
    % if c.isNamespace == 'true':
<% continue %>
    % endif
    % if c.abstract != "true":
    //implicitly_convertible<${c.name}Wrapper*,${c.name}*>();
    % endif
    implicitly_convertible<${c.name}*,${c.baseClassName}*>();
    class_<std::vector<${c.name}*>>("${c.name}List").def(vector_indexing_suite<std::vector<${c.name}*>>());
% endfor
}