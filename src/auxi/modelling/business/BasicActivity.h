#ifndef BASICACTIVITY_H
#define BASICACTIVITY_H



#include "TransactionTemplate.h"
#include "Clock.h"
#include "Activity.h"
#include "boost/date_time/posix_time/posix_time.hpp"
#include <vector>
#include <map>
#include <tuple>
#include <set>


// Forward declarations.
//
namespace auxi { namespace modelling { namespace business {
    class BasicActivity;
}}}

namespace auxi { namespace modelling { namespace business {
    using namespace auxi::core;

    // Declare classes
    //
    class BasicActivity : public Activity
    {
        public:
            BasicActivity();
            BasicActivity(std::string name, std::string description) : Activity(name, description)
            {
                initialize();
            };
            ~BasicActivity();
            BasicActivity(const BasicActivity& other);

            friend bool operator==(const BasicActivity& lhs, const BasicActivity& rhs);
            friend bool operator!=(const BasicActivity& lhs, const BasicActivity& rhs);
            friend std::ostream& operator<<(std::ostream&, const BasicActivity&);

            bool IsValid() const { return true; }
            BasicActivity* Clone() const { return new BasicActivity(*this); }


            void initialize();

            virtual bool OnExecute_MeetExecutionCriteria(int executionMonth);

            void prepare_to_run(Clock* clock, int totalIntervalsToRun);

            void run(Clock* clock, int ix_interval, auxi::modelling::financial::double_entry_system::GeneralLedger* generalLedger);
            boost::posix_time::ptime GetDate() const;
            void SetDate(boost::posix_time::ptime date);

            auxi::modelling::financial::double_entry_system::TransactionTemplate& GetTransactionTemplate();
            void SetTransactionTemplate(auxi::modelling::financial::double_entry_system::TransactionTemplate& transactionTemplate);

            double GetAmount() const;
            void SetAmount(double amount);


        protected:
	        boost::posix_time::ptime m_date = boost::posix_time::time_from_string("1500-01-01 00:00:00");
	        auxi::modelling::financial::double_entry_system::TransactionTemplate m_transactionTemplate;
	        double m_amount = 0.0;

        private:
    };
}}}
#endif