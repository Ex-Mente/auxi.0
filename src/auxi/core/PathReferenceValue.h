#ifndef PATHREFERENCEVALUE_H
#define PATHREFERENCEVALUE_H
#include <string>

namespace auxi{ namespace core
{
    template<typename T> class PathReferenceValue;
    template<typename T>
    bool operator==(const PathReferenceValue<T> rhs, const PathReferenceValue<T>& lhs)
    {
        return rhs.Path() == lhs.Path();
    }

    template<typename T>
    class PathReferenceValue
    {
    public:
        PathReferenceValue();
        PathReferenceValue(std::string path) : m_Path(path) {}
        PathReferenceValue(const PathReferenceValue<T>& other);
        ~PathReferenceValue();

        friend bool operator==<>(const PathReferenceValue<T> rhs, const PathReferenceValue<T>& lhs);

        PathReferenceValue* Clone() { return new PathReferenceValue(*this); }

        T GetValue() const { return m_value; }

        std::string GetPath() const { return m_Path; }
        void SetPath(std::string val) { m_Path = val; }
    protected:
    private:
        T m_value;
        std::string m_Path;
    };
}}
#endif // PATHREFERENCEVALUE_H
