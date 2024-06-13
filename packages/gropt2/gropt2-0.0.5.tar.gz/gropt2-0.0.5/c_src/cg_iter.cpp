#include <iostream> 
#include <string>
#include <math.h>  
#include "Eigen/Dense"
#include <vector>  

#include "op_main.hpp"
#include "cg_iter.hpp"
#include "logging.hpp"

#define N_HIST_MAX 100000

namespace Gropt {

void get_AtAx(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &X, Eigen::VectorXd &Ax)
{
    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->add2AtAx(X, Ax);
    }

    for (int i = 0; i < all_obj.size(); i++) {
        all_obj[i]->add2AtAx(X, Ax);
    }
}

CG_Iter::CG_Iter(int N, int max_iter) 
    : N(N), max_iter(max_iter)
{
    b.setZero(N);
    Ax.setZero(N);
    Ap.setZero(N);
    r.setZero(N);
    p.setZero(N); 
}

Eigen::VectorXd CG_Iter::solve(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &x0, int iiter)
{
    // std::ostringstream savename;
    
    // savename.str("");
    // savename << "cg_x0_ii" << iiter << ".bin" ;
    // write_vector_xd(savename.str(), x0);

    // for (int i = 0; i < all_op.size(); i++) {
    //     if (all_op[i]->name == "Moments") {
    //         for (int j = 0; j < all_op[i]->A.rows(); j++) {
    //             savename.str("");
    //             savename << "cg_A_row" << j << "_ii" << iiter << ".bin" ;
    //             write_vector_xd(savename.str(), all_op[i]->A.row(j));
    //         }
    //     }
    // }
    
    double rnorm0;
    double bnorm0;
    double tol0;
    double pAp;
    double alpha;
    double beta;
    double gamma;
    double res;
    
    Ax.setZero();
    Ap.setZero();

    b.setZero();
    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->add2b(b);
    }

    for (int i = 0; i < all_obj.size(); i++) {
        all_obj[i]->obj_add2b(b);
    }

    // savename.str("");
    // savename << "cg_Atb_ii" << iiter << ".bin" ;
    // write_vector_xd(savename.str(), b);

    get_AtAx(all_op, all_obj, x0, Ax);

    // savename.str("");
    // savename << "cg_AtAx_ii" << iiter << ".bin" ;
    // write_vector_xd(savename.str(), Ax);

    r = (b - Ax);
    rnorm0 = r.norm();
    bnorm0 = b.norm();

    tol0 = std::max(0.1*rnorm0/bnorm0, 1.0e-12);
    if (iiter > 3) {
        tol = std::min(tol0, tol);  // Dont allow tol to grow from last run of CG
    } else {
        tol = tol0;
    }
    
    p = r;
    gamma = r.dot(r);


    // Start actual CG
    int ii;
    for (ii = 0; ii < max_iter; ii++) {
        Ap.setZero();
        get_AtAx(all_op, all_obj, p, Ap);  // Ap = A*p

        gamma = r.dot(r);
        pAp = p.dot(Ap);
        alpha = gamma / pAp;

        if ((pAp == 0) || (alpha < 0)) {break;}
        
        x0 += alpha * p;

        if ((ii > 0) && (ii%10 == 0)) {
            Ax.setZero();
            get_AtAx(all_op, all_obj, x0, Ax);
            r = (b - Ax);
        } else {
            r -= alpha * Ap;
        }
        

        res = r.norm()/bnorm0;

        if (res <= tol) {break;}

        beta = r.dot(r) / gamma;

        p = beta * p + r;
    }

    n_iter = ii+1;
    hist_n_iter.push_back(n_iter);

    log_print(LOG_DEBUG, "CG   iiter: %d  n_iter: %d   tol: %.5e   res: %.5e", iiter, n_iter, tol, res);
    
    // savename.str("");
    // savename << "cg_x1_ii" << iiter << ".bin" ;
    // write_vector_xd(savename.str(), x0);

    return x0;
}

int CG_Iter::get_n_iter()
{
    return n_iter;
}

}  // end namespace Gropt