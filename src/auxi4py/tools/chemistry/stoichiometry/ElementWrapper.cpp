
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Element.h"

using namespace boost::python;
using namespace auxi::tools::chemistry;

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



struct ElementWrapper : Element, wrapper<Element>
{
};

void export_auxi_tools_chemistry_Element()
{
  // Python C++ mappings



    class_<ElementWrapper, Element*, bases<NamedObject>>("Element", "An element in the periodic table.", init<>())
	.def(init<std::string, std::string>())
	.def(self == self)
    
	.def("to_string", &Element::to_string)

	.add_property("period", &Element::GetPeriod, &Element::SetPeriod, "Period to which the element belongs.")

	.add_property("group", &Element::GetGroup, &Element::SetGroup, "Group to which the element belongs.")

	.add_property("atomic_number", &Element::GetAtomic_number, &Element::SetAtomic_number, "Number of protons in the element's nucleus.")

	.add_property("symbol", &Element::GetSymbol, &Element::SetSymbol, "Element's symbol.")

	.add_property("molar_mass", &Element::GetMolar_mass, &Element::SetMolar_mass, "[kg/kmol] Element's standard atomic mass.")
    ;

    //implicitly_convertible<ElementWrapper*,Element*>();
    implicitly_convertible<Element*,NamedObject*>();
    class_<std::vector<Element*>>("ElementList").def(vector_indexing_suite<std::vector<Element*>>());
}