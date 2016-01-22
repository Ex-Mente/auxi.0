#ifndef ${filename.upper()}_H
#define ${filename.upper()}_H

<% baseclasses = {} %>
% for c in classes:
% if c.baseClassName != "":
<% baseclasses[c.baseClassName] = c.baseClassName %>
% endif
% for a_i in c.additional_includes:
% if a_i[0] == "<":
#include ${a_i}
% else:
#include "${a_i}.h"
% endif
% endfor
% endfor
% for key in baseclasses:
#include "${key}.h"
% endfor
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>

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
# Introspection on types
def isTypeList(type):
    if type[:12] == "std::vector<":
        return True
    return False
def isTypeMap(type):
    if type[:9] == "std::map<":
        return True
    return False
def isTypeTuple(type):
    if type[:11] == "std::tuple<":
        return True
    return False
def shouldWrapFunction(f):
  if f.private:
    return False
  for p in f.params:
    if isTypeList(p[1]) or isTypeMap(p[1]):
        return True
  return False
%><%
namespace_decl = ""
namespace_end = ""
isNamespaceCount = 0
for ns in namespace_parts:
    namespace_decl += "namespace " + ns + " { "
    namespace_end += "}"
%>
% for c in classes:
    % for ns in c.additional_namepace_usings:
using ${ns};
    % endfor
    % if c.isNamespace == 'true':
        <% isNamespaceCount = isNamespaceCount + 1 %>
${namespace_decl}namespace ${c.name[:1].lower() + c.name[1:]} {
##/////////////////// NAMESPACE ${c.name} ///////////////////
% for f in c.functions:
<%
func_signature = f.returnType + " " + f.name + "("
if f.virtual in ["required","true"]:
  func_signature = "virtual " + func_signature
if len(f.params) > 0:
  func_signature = func_signature + f.params[0][1] + " " + f.params[0][0]
  if f.params[0][2] is not None:
    if f.params[0][1] == "std::string":
        func_signature = func_signature + " = \"" + f.params[0][2] + "\""
    else: func_signature = func_signature + " = " + f.params[0][2]
for pm in f.params[1:]:
  func_signature = func_signature + ", " + pm[1] + " " + pm[0]
  if pm[2] is not None:
    if pm[1] == "std::string":
        func_signature = func_signature + " = \"" + pm[2] + "\""
    else: func_signature = func_signature + " = " + pm[2]
if f.virtual == "required":
  func_signature = func_signature + ") = 0;"
else:
  func_signature = func_signature + ");"
%>
${func_signature}
% endfor
//// Property accessor methods ////
% for p in c.properties:
% if p.private == "true":
<% continue %>
    % endif
% if p.isList:
    ${p.type}& Get${p.name}();
    % endif
% if not p.isList:
      % if is_ComplexClass(p, classes, namespace_name):
% if p.get != "false":
    ${p.type}& Get${p.name}();
% endif
% if p.set != "false":
    void Set${p.name}(${p.type}& ${p.namelower});
% endif
  % else:
% if p.get != "false":
  % if p.get == "custom":
    ${p.type} Get${p.name}();
  % else:
    ${p.type} Get${p.name}();
  % endif
% endif
% if p.set != "false":
    void Set${p.name}(${p.type} ${p.namelower});
% endif
  % endif
    % endif
% endfor

//// Properties ////
% for p in c.properties:
  % if not(p.name=="Name") and not(p.name=="Description"):
    % if is_ComplexClass(p, classes, namespace_name) or p.default == None:
      % if p.type == "std::string":
extern ${p.type} m_${p.namelower};
      % else:
extern ${p.type} m_${p.namelower};
      % endif
    % elif is_Enum(p, enums):
extern ${p.type} m_${p.namelower};
    % else:
      % if p.type == "boost::posix_time::ptime":
extern ${p.type} m_${p.namelower};
      % else:
extern ${p.type} m_${p.namelower};
      % endif
    % endif
    % if p.optional:
extern bool m_${p.namelower}Specified
    % endif
  % endif
% endfor
##///////////////////////////////////////////////////////////
${namespace_end}}
    % endif
% endfor
% if isNamespaceCount != len(classes):
// Forward declarations.
//
${namespace_decl}
% for c in classes:
    % if c.isNamespace != 'true':
    class ${c.name};
% if c.forwardDeclareClasses is not None:
    class ${c.forwardDeclareClasses};
% endif
% endif
% endfor
${namespace_end}

${namespace_decl}
    using namespace auxi::core;
    % if len(enums) > 0:

    // Declare enums
    //
    % for e in enums:
    namespace ${e.name}
    {
        enum ${e.name}
        {
        % for v in e.values:
	        ${v},
        % endfor
        };
    }
    % endfor
    % endif

    // Declare classes
    //
    % for c in classes:
    % if c.isNamespace != 'true':
    class ${c.name} : public ${c.baseClassName}
    {
	% if c.custom_code is not None:
        ${c.custom_code}
	% endif
        public:
% if c.baseClassName == "Object":
            ${c.name}() : ${c.baseClassName}()
            {
                % if c.constructor_init_function not in [None, ""]:
                ${c.constructor_init_function}();
                % endif
            };
% else:
            ${c.name}();
            <%
            define_named_const = True
            for f in c.functions:
                if f.custom_constructor:
                    define_named_const = False
                    break
            %>
            % if define_named_const:
            ${c.name}(std::string name, std::string description) : ${c.baseClassName}(name, description)
            {
                % if c.constructor_init_function not in [None, ""]:
                ${c.constructor_init_function}();
                % endif
            };
            % endif
% endif
            ~${c.name}();
            ${c.name}(const ${c.name}& other);

            friend bool operator==(const ${c.name}& lhs, const ${c.name}& rhs);
            friend bool operator!=(const ${c.name}& lhs, const ${c.name}& rhs);
            friend std::ostream& operator<<(std::ostream&, const ${c.name}&);

            bool IsValid() const { return true; }
            % if c.abstract != "true":
            ${c.name}* Clone() const { return new ${c.name}(*this); }
            % endif

	    ## User defined functions
	    % for f in c.functions:
	    % if f.private == "true":
<% continue %>
            % endif
	      <%
            	func_signature = f.returnType + " " + f.name + "("
            	if f.virtual in ["required","true"]:
            	  func_signature = "virtual " + func_signature
            	if len(f.params) > 0:
            	  func_signature = func_signature + f.params[0][1] + " " + f.params[0][0]
            	for pm in f.params[1:]:
            	  func_signature = func_signature + ", " + pm[1] + " " + pm[0]
            	  if pm[2] is not None:
                    if pm[1] == "std::string":
                      func_signature = func_signature + " = \"" + pm[2] + "\""
                    else: func_signature = func_signature + " = " + pm[2]
                if f.virtual == "required":
            	  func_signature = func_signature + ") = 0;"
            	else:
            	  func_signature = func_signature + ");"
	      %>
            ${func_signature}
            % endfor
	    ## Property accessor methods
	    % for p in c.properties:
	    % if p.private == "true":
<% continue %>
            % endif
	    % if p.isList:
            ${p.type}& Get${p.name}();
            % endif
	    % if not p.isList:
              % if is_ComplexClass(p, classes, namespace_name):
		% if p.get != "false":
            ${p.type}& Get${p.name}();
		% endif
		% if p.set != "false":
            void Set${p.name}(${p.type}& ${p.namelower});
		% endif
	      % else:
		% if p.get != "false":
		  % if p.get == "custom":
            ${p.type} Get${p.name}();
		  % else:
            ${p.type} Get${p.name}() const;
		  % endif
		% endif
		% if p.set != "false":
            void Set${p.name}(${p.type} ${p.namelower});
		% endif
	      % endif
            % endif

	    % endfor

        protected:
	% for p in c.properties:
	  % if not(p.name=="Name") and not(p.name=="Description"):
	    % if is_ComplexClass(p, classes, namespace_name) or p.default == None:
	      % if p.type == "std::string":
	        ${p.type} m_${p.namelower} = "";
	      % else:
	        ${p.type} m_${p.namelower};
	      % endif
	    % elif is_Enum(p, enums):
	        ${p.type} m_${p.namelower} = ${p.type}::${p.default};
	    % else:
	      % if p.type == "boost::posix_time::ptime" and p.default not in ["boost::posix_time::min_date_time", "boost::posix_time::max_date_time"]:
	        ${p.type} m_${p.namelower} = boost::posix_time::time_from_string("${p.default}");
          % elif p.type == "std::string":
            ${p.type} m_${p.namelower} = "${p.default}";
	      % else:
	        ${p.type} m_${p.namelower} = ${p.default};
	      % endif
	    % endif
        % if p.optional:
            bool m_${p.namelower}Specified = false;
        % endif
	  % endif
	% endfor

        private:
        % for f in c.functions:
	    % if f.private == "true":
	      <%
		func_signature = f.returnType + " " + f.name + "("
		if f.virtual in ["required","true"]:
		  func_signature = "virtual " + func_signature
		if len(f.params) > 0:
		  func_signature = func_signature + f.params[0][1] + " " + f.params[0][0]
		for pm in f.params[1:]:
		  func_signature = func_signature + ", " + pm[1] + " " + pm[0]
		  if pm[2] is not None:
                    func_signature = func_signature + " = " + pm[2]
                if f.virtual == "required":
		  func_signature = func_signature + ") = 0;"
		else:
		  func_signature = func_signature + ");"
	      %>
            ${func_signature}
            % endif
	% endfor
    };
    % endif
    % endfor
${namespace_end}
% endif
#endif