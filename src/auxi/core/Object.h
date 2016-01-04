#pragma once

#include "IObject.h"
#include <memory>
#include <map>
#include <string>
#include <sstream>
#include "Utilities.h"

namespace auxi{ namespace core
{
    template <typename T>
    std::string to_string(T value)
    {
      //create an output string stream
      std::ostringstream os ;

      //throw the value into the string stream
      os << value ;

      //convert the string stream into a string and return
      return os.str() ;
    }

    class Object : public IObject
    {
    public:
        /*typedef std::shared_ptr<Object> (*ObjectConstructorPtr)( const std::string& dict);
        typedef std::map<std::string, ObjectConstructorPtr> ObjectConstructorTable;

        static ObjectConstructorTable* ObjectConstructorTablePtr_;

        static void constructObjectConstructorTables();
        static void destroyObjectConstructorTables();
        */
        Object() {}
        virtual ~Object();

        //virtual bool IsValid() const = 0;
        //virtual Object* Clone() const = 0;

        /*
        static std::shared_ptr<Object> New(const std::string&);

        template<class DerivedType>
        class addObjectConstructorToTable
        {
        public:

            static std::shared_ptr<Object> New ( const std::string& dict)
            {
                return std::shared_ptr<Object>(new DerivedType (dict));
                //return Object(new DerivedType (dict));
            }

            addObjectConstructorToTable(std::string lookup = DerivedType::type())
            {
                constructObjectConstructorTables();
                ObjectConstructorTablePtr_->insert(std::pair<std::string, ObjectConstructorPtr>(lookup, New));
            }

            ~addObjectConstructorToTable()
            {
                destroyObjectConstructorTables();
            }
        };*/
    };
}}
