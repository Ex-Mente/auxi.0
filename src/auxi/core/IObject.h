#include <string>

#include <boost/uuid/uuid.hpp>
//#include <boost/uuid/random_generator.hpp>
//#include <boost/uuid/uuid_io.hpp>
//#include <boost/log/trivial.hpp>

namespace auxi{ namespace core
{
class ModelingProject;
class Object;
class IObject
{
public:
    virtual ~IObject();
    /// <summary>
    /// Gets the globally unique id of this Object.
    /// </summary>
    //boost::uuids::uuid uuid;

    /// <summary>
    /// Gets or sets a reference to the model the Object belongs to.
    /// </summary>
    /// <value>
    /// The model.
    /// </value>
    ModelingProject* project;

    /// <summary>
    /// Gets or sets a reference to the Object's parent.
    /// </summary>
    /// <value>
    /// The parent.
    /// </value>
    Object* parent;

    /// <summary>
    /// Gets the path of the Object.
    /// </summary>
    std::string path;

    /// <summary>
    /// Clones this instance.
    /// </summary>
    /// <returns></returns>
    //IObject Clone();

    /// <summary>
    /// Returns the path of the specified child Object. This method is called by a child Object, because a child Object cannot determine its path by itself. It
    /// needs its parent to tell it what its path is.
    /// </summary>
    /// <param name="child">The child Object for which to calculate the path.</param>
    /// <returns>The path of the child Object.</returns>
    //virtual std::string GetChildObjectPath(Object* child) { return ""; };
};
}}
