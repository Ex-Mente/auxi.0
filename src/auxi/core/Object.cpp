#include "Object.h"

using namespace auxi::core;

Object::~Object()
{
}

/*
void Object::constructObjectConstructorTables()
{
    static bool constructed = false;
    // this is necessary because it will be called many times
    if (!constructed)
    {
        Object::ObjectConstructorTablePtr_ = new Object::ObjectConstructorTable();
        constructed = true;
    }
}

void Object::destroyObjectConstructorTables()
{
    if (Object::ObjectConstructorTablePtr_)
    {
        delete Object::ObjectConstructorTablePtr_;
        Object::ObjectConstructorTablePtr_ = NULL;
    }
}

std::shared_ptr<Object> Object::New(const std::string& dict)
{
    // omitting error catching and debug statements

    //std::string DerivedType(dict.lookup("type"));
    std::string DerivedType(dict);

    typename ObjectConstructorTable::iterator cstrIter
        = ObjectConstructorTablePtr_->find(DerivedType);

    return cstrIter->second(dict);;
    //return cstrIter()(dict);
}
*/
