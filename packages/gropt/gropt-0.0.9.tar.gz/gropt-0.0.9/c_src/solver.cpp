
#include "solver.hpp"

namespace Gropt {

void Solver::get_AtAx_combined(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &X, Eigen::VectorXd &Ax)
{
    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->add2AtAx(X, Ax);
    }

    for (int i = 0; i < all_obj.size(); i++) {
        all_obj[i]->add2AtAx(X, Ax);
    }
}

void Solver::get_Atb_combined(std::vector<GroptOperator*> all_op, std::vector<GroptOperator*> all_obj, Eigen::VectorXd &b)
{
    for (int i = 0; i < all_op.size(); i++) {
        all_op[i]->add2b(b);
    }

    for (int i = 0; i < all_obj.size(); i++) {
        all_obj[i]->obj_add2b(b);
    }
}


std::vector<double> Solver::get_stats(GroptParams &gparams, Eigen::VectorXd &X) {

    double xnorm = X.norm();
    double Axnorm = 0;
    double rnorm = 0;

    for (int i = 0; i < gparams.all_op.size(); i++) {
        gparams.all_op[i]->Ax_temp.setZero();
        gparams.all_op[i]->forward(X, gparams.all_op[i]->Ax_temp, 1, 1, false);

        Axnorm += gparams.all_op[i]->Ax_temp.squaredNorm();
        rnorm += (gparams.all_op[i]->Ax_temp - gparams.all_op[i]->get_b()).squaredNorm();
    }

    Axnorm = sqrt(Axnorm);
    rnorm = sqrt(rnorm);

    std::vector<double> out{xnorm, Axnorm, rnorm};

    return out;
}


std::vector<double> Solver::get_stats_normal(GroptParams &gparams, Eigen::VectorXd &X) {

    double xnorm = X.norm();

    Eigen::VectorXd temp_Ax;
    Eigen::VectorXd temp_b;

    temp_Ax.setZero(gparams.N);
    temp_b.setZero(gparams.N);

    get_Atb_combined(gparams.all_op, gparams.all_obj, temp_b);
    get_AtAx_combined(gparams.all_op, gparams.all_obj, X, temp_Ax);

    double Axnorm = temp_Ax.norm();
    double rnorm = (temp_Ax - temp_b).norm();

    std::vector<double> out{xnorm, Axnorm, rnorm};

    return out;
}


void Solver::get_residual(GroptParams &gparams, Eigen::VectorXd &X, int mode) {
    
    std::vector<double> all_resid;

    for (int i = 0; i < gparams.all_op.size(); i++) {
        gparams.all_op[i]->Ax_temp.setZero();
        gparams.all_op[i]->forward(X, gparams.all_op[i]->Ax_temp, 2, 1, false);

        if (gparams.all_op[i]->weight.size() == 1) {
            double resid = (gparams.all_op[i]->Ax_temp - gparams.all_op[i]->get_b()).norm();
            all_resid.push_back(resid);
        } else {
            Eigen::VectorXd resid = (gparams.all_op[i]->Ax_temp - gparams.all_op[i]->get_b());
            for (int j = 0; j < gparams.all_op[i]->weight.size(); j++) {
                all_resid.push_back(resid(j));
            }
        }
    }

    for (int i = 0; i < gparams.all_obj.size(); i++) {
        gparams.all_obj[i]->Ax_temp.setZero();
        gparams.all_obj[i]->forward(X, gparams.all_obj[i]->Ax_temp, true, 1, false);
        
        if (gparams.all_obj[i]->weight.size() == 1) {
            double resid = (gparams.all_obj[i]->Ax_temp - gparams.all_obj[i]->get_b()).norm();
            all_resid.push_back(resid);
        } else {
            Eigen::VectorXd resid = (gparams.all_obj[i]->Ax_temp - gparams.all_obj[i]->get_b());
            for (int j = 0; j < gparams.all_obj[i]->weight.size(); j++) {
                all_resid.push_back(resid(j));
            }
        }
    }

    if (mode == 0) {
        gparams.debugger.hist_pre_resid.push_back(all_resid);
    } else if (mode == 1) {
        gparams.debugger.hist_post_resid.push_back(all_resid);
    }

}

int Solver::get_n_iter()
{
    return n_iter;
}

}