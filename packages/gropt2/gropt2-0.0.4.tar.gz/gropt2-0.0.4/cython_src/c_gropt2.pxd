from libcpp.string cimport string
from libcpp.vector cimport vector

cdef extern from "gropt_params.hpp" namespace "Gropt":

    cdef cppclass GroptParams:

        GroptParams() except +

        int grw_interval
        int grw_start
        double grw_scale

        double rw_scalelim
        double rw_interval
        double rw_eps
        double e_corr
        double weight_min
        double weight_max

        int cg_niter
        double d_obj_thresh

        double total_n_feval
        double total_n_iter

        int final_good

        int N_iter
        string solver_type

        void init_N(int N_in, double _dt)
        void init_simple_diffusion(double _dt, double T_90, double T_180, double T_readout, double TE)

        void add_gmax(double gmax)
        void add_smax(double smax)

        void add_moment(double order, double target)

        void add_obj_bval(double weight)
        void add_op_bval(double _bval)

        void add_op_eddy(double _lam_in, double _tol_in)
        void add_op_eddy(double _lam_in)
        void add_op_PNS(double stim_thresh)

        void optimize()
        void optimize(int N_X0, double *_X0)

        void get_out(vector[double] &out_vec)

        void set_verbose(int level)


cdef extern from "gropt_utils.hpp" namespace "Gropt":
    
    double get_bval(int N, double *G_in, int idx_inv, double dt)