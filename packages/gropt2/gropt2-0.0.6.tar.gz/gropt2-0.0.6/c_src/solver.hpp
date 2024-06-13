#ifndef SOLVER_H
#define SOLVER_H

#include <iostream> 
#include <string>
#include <vector>
#include "Eigen/Dense"

#include "op_main.hpp"

namespace Gropt {

class Solver
{
    public:
        std::vector<int> hist_n_iter;  
        int n_iter;
        
        virtual int get_n_iter() = 0;
        virtual Eigen::VectorXd solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter) = 0;
        
};

}  // end namespace Gropt

#endif