
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#include <boost/python/operators.hpp>
#include "Element.h"
#include "Stoichiometry.h"

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


using namespace auxi::tools::chemistry::stoichiometry;







BOOST_PYTHON_FUNCTION_OVERLOADS(Stoichiometrymolar_mass, molar_mass, 0, 1)


    
list element_mass_fractionsWrapper(std::string compound, list elements)
{
    
	std::vector<std::string> elements_prepped;
	for(int i=0; i<len(elements); ++i) elements_prepped.push_back(extract<std::string>(elements[i]));
		
    auto result = element_mass_fractions(compound, elements_prepped);
    return to_python_list(result);
}
    
list elementsWrapper(list compounds)
{
    
	std::vector<std::string> compounds_prepped;
	for(int i=0; i<len(compounds); ++i) compounds_prepped.push_back(extract<std::string>(compounds[i]));
		
    auto result = elements(compounds_prepped);
    return to_python_list(result);
}
    
list stoichiometry_coefficientsWrapper(std::string compound, list elements)
{
    
	std::vector<std::string> elements_prepped;
	for(int i=0; i<len(elements); ++i) elements_prepped.push_back(extract<std::string>(elements[i]));
		
    auto result = stoichiometry_coefficients(compound, elements_prepped);
    return to_python_list(result);
}

void export_auxi_tools_chemistry_Stoichiometry()
{
  // Python C++ mappings


    using namespace auxi::tools::chemistry::stoichiometry;
/////////////////// NAMESPACE Stoichiometry ///////////////////
    
    
    
    
    
    
    
    
    
    
    def("amount", amount, args("compound", "mass"), "Calculate the number of moles in the specified mass of a chemical compound.\n"
"\n"
":param compound: Formula and phase of a compound, e.g. \"Fe2O3[S1]\". The phase may be omitted.\n"
":param mass: [kg]\n"
"\n"
":return: Amount. [kmol]");
    
    def("mass", mass, args("compound", "amount"), "Calculate the mass of the specified amount of a chemical compound.\n"
"\n"
":param compound: Formula and phase of a compound, e.g. \"Fe2O3[S1]\". The phase may be omitted.\n"
":param amount: [kmol]\n"
"\n"
":return: [kg]");
    
    def("convert_compound", convert_compound, args("mass", "source", "target", "element"), "Convert the specified mass of the source compound to the target using element as basis.\n"
"\n"
":param mass: Mass of from_compound. [kg]\n"
":param source: Formula and phase of the original compound, e.g. \"Fe2O3[S1]\".\n"
":param target: Formula and phase of the target compound, e.g. \"Fe[S1]\".\n"
":param element: Element to use as basis for the conversion, e.g. \"Fe\" or \"O\".\n"
"\n"
":return: Mass of to_compound. [kg]");
    
    def("element_mass_fraction", element_mass_fraction, args("compound", "element"), "Determine the mass fraction of an element in a chemical compound.\n"
"\n"
":param compound: Formula of the chemical compound, \"FeCr2O4\".\n"
":param element: Element, e.g. \"Cr\".\n"
"\n"
":return: Element mass fraction.");
    
    def("element_mass_fractions", element_mass_fractionsWrapper, args("compound", "elements"), "Determine the mass fractions of a list of elements in a chemical compound.\n"
"\n"
":param compound: Formula and phase of a chemical compound, e.g. \"Fe2O3[S1]\".\n"
":param elements: List of elements, [\"Si\", \"O\", \"Fe\"].\n"
"\n"
":return: Mass fractions.");
    
    def("elements", elementsWrapper, args("compounds"), "Determine the set of elements present in a list of chemical compounds.\\n\\nThe list of elements is sorted alphabetically.\n"
"\n"
":param compounds: List of elements.\n"
"\n"
":return: ");
    
    def("molar_mass", molar_mass, Stoichiometrymolar_mass(args("compound"), "Determine the molar mass of a chemical compound. The molar mass is usually the mass of one mole of the substance, but here it is the mass of 1000 moles, since the mass unit used in pmpy is kg.\n"
"\n"
":param compound: Formula of a chemical compound, e.g. \"Fe2O3\".\n"
"\n"
":return: Molar mass. [kg/kmol]"));
    
    def("stoichiometry_coefficient", stoichiometry_coefficient, args("compound", "element"), "Determine the stoichiometry coefficient of an element in a chemical compound.\n"
"\n"
":param compound: Formula of a chemical compound, e.g. \"SiO2\".\n"
":param element: Element, e.g. \"Si\".\n"
"\n"
":return: Stoichiometry coefficient.");
    
    def("stoichiometry_coefficients", stoichiometry_coefficientsWrapper, args("compound", "elements"), "Determine the stoichiometry coefficients of the specified elements in the specified chemical compound.\n"
"\n"
":param compound: Formula of a chemical compound, e.g. \"SiO2\".\n"
":param elements: List of elements, e.g. [\"Si\", \"O\", \"C\"].\n"
"\n"
":return: List of stoichiometry coefficients.");
////////////////////////////////////////////////////

}