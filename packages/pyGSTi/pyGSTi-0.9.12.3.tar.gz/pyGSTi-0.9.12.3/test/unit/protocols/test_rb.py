from ..util import BaseCase

import numpy as _np

import pygsti
from pygsti.protocols import rb as _rb
from pygsti.processors import CliffordCompilationRules as CCR
from pygsti.processors import QubitProcessorSpec as QPS

class TestCliffordRBDesign(BaseCase):

    def setUp(self):
        self.num_qubits = 2
        self.qubit_labels = ['Q'+str(i) for i in range(self.num_qubits)]
        
        gate_names = ['Gi', 'Gxpi2', 'Gxmpi2', 'Gypi2', 'Gympi2', 'Gcphase']
        availability = {'Gcphase':[('Q'+str(i),'Q'+str((i+1) % self.num_qubits)) for i in range(self.num_qubits)]}

        self.pspec = pygsti.processors.QubitProcessorSpec(self.num_qubits, gate_names, availability=availability,
                                                          qubit_labels=self.qubit_labels)
        self.compilations = {
            'absolute': CCR.create_standard(self.pspec, 'absolute', ('paulis', '1Qcliffords'), verbosity=0),
            'paulieq': CCR.create_standard(self.pspec, 'paulieq', ('1Qcliffords', 'allcnots'), verbosity=0)
        }

        gate_names_1Q = gate_names[:-1]
        self.qubit_labels1Q = ['Q0']
        self.pspec1Q = pygsti.processors.QubitProcessorSpec(1, gate_names_1Q, qubit_labels=self.qubit_labels1Q)
        self.compilations1Q = {
            'absolute': CCR.create_standard(self.pspec1Q, 'absolute', ('paulis', '1Qcliffords'), verbosity=0),
            'paulieq': CCR.create_standard(self.pspec1Q, 'paulieq', ('1Qcliffords', 'allcnots'), verbosity=0)
        }

        # TODO: Test a lot of these, currently just the default from the tutorial
        # Probably as pytest mark parameterize for randomizeout, compilerargs?
        self.depths = [0, 2]#, 4, 8]
        self.circuits_per_depth = 5
        self.qubits = ['Q0', 'Q1']
        self.citerations = 20
        self.randomizeout = True
        self.interleaved_circuit = None
        self.compiler_args = ()
        self.seed = 2021
        self.verbosity = 0

    def test_design_construction(self):
        num_mp_procs = 4
        
        serial_design = _rb.CliffordRBDesign(
            self.pspec, self.compilations, self.depths, self.circuits_per_depth, qubit_labels=self.qubits,
            randomizeout=self.randomizeout, interleaved_circuit=self.interleaved_circuit,
            citerations=self.citerations, compilerargs=self.compiler_args, seed=self.seed,
            verbosity=self.verbosity, num_processes=1)
        
        # Test parallel circuit generation works and is seeded properly
        mp_design = _rb.CliffordRBDesign(
            self.pspec, self.compilations, self.depths, self.circuits_per_depth, qubit_labels=self.qubits,
            randomizeout=self.randomizeout, interleaved_circuit=self.interleaved_circuit,
            citerations=self.citerations, compilerargs=self.compiler_args, seed=self.seed,
            verbosity=self.verbosity, num_processes=num_mp_procs)

        # for sd_circ, md_circ in zip(serial_design.all_circuits_needing_data, mp_design.all_circuits_needing_data):
        #     if str(sd_circ) != str(md_circ):
        #         print('Mismatch found!')
        #         print('  Serial circuit:   ' + str(sd_circ))
        #         print('  Parallel circuit: ' + str(md_circ))

        self.assertTrue(all([str(sd) == str(md) for sd, md in zip(serial_design.all_circuits_needing_data,
                                                        mp_design.all_circuits_needing_data)]))

        tmodel = pygsti.models.create_crosstalk_free_model(self.pspec)

        [[self.assertAlmostEqual(c.simulate(tmodel)[bs],1.) for c, bs in zip(cl, bsl)] for cl, bsl in zip(mp_design.circuit_lists, mp_design.idealout_lists)]

    def test_deterministic_compilation(self):        
        # TODO: Figure out good test for this. Full circuit is a synthetic idle, we need to somehow check the non-inverted
        # Clifford is the same as the random case?
        abs_design = _rb.CliffordRBDesign(
            self.pspec1Q, self.compilations1Q, self.depths, self.circuits_per_depth, qubit_labels=self.qubit_labels1Q,
            randomizeout=self.randomizeout, interleaved_circuit=self.interleaved_circuit,
            citerations=self.citerations, compilerargs=self.compiler_args, seed=self.seed,
            verbosity=self.verbosity, exact_compilation_key='absolute')
        
        peq_design = _rb.CliffordRBDesign(
            self.pspec1Q, self.compilations1Q, self.depths, self.circuits_per_depth, qubit_labels=self.qubit_labels1Q,
            randomizeout=self.randomizeout, interleaved_circuit=self.interleaved_circuit,
            citerations=self.citerations, compilerargs=self.compiler_args, seed=self.seed,
            verbosity=self.verbosity, exact_compilation_key='paulieq')

        # Testing a non-standard (but unrealistic) compilation
        rule_dict = {f'C{i}': (_np.eye(2), pygsti.circuits.Circuit([], (0,))) for i in range(24)}
        compilations = self.compilations1Q.copy()
        compilations["idle"] = pygsti.processors.CompilationRules(rule_dict)
        idle_design = _rb.CliffordRBDesign(
            self.pspec1Q, compilations, self.depths, self.circuits_per_depth, qubit_labels=self.qubit_labels1Q,
            randomizeout=False, interleaved_circuit=self.interleaved_circuit,
            citerations=self.citerations, compilerargs=self.compiler_args, seed=self.seed,
            verbosity=self.verbosity, exact_compilation_key='idle')

        # All circuits should be the empty circuit (since we've turned off randomizeout)
        for clist in idle_design.circuit_lists:
            self.assertTrue(set(clist) == set([pygsti.circuits.Circuit([], self.qubit_labels1Q)]))

        # Also a handy place to test native gate counts since it should be 0
        avg_gate_counts = idle_design.average_native_gates_per_clifford()
        for v in avg_gate_counts.values():
            self.assertTrue(v == 0)

class TestDirectRBDesign(BaseCase):

    def setUp(self):
        self.num_qubits = 2
        self.qubit_labels = ['Q'+str(i) for i in range(self.num_qubits)]
        
        gate_names = ['Gxpi2', 'Gxmpi2', 'Gypi2', 'Gympi2', 'Gcphase']
        availability = {'Gcphase':[('Q'+str(i),'Q'+str((i+1) % self.num_qubits)) for i in range(self.num_qubits)]}

        self.pspec = pygsti.processors.QubitProcessorSpec(self.num_qubits, gate_names, availability=availability,
                                                          qubit_labels=self.qubit_labels, geometry='line')
        self.compilations = {
            'absolute': CCR.create_standard(self.pspec, 'absolute', ('paulis', '1Qcliffords'), verbosity=0),
            'paulieq': CCR.create_standard(self.pspec, 'paulieq', ('1Qcliffords', 'allcnots'), verbosity=0)
        }


        # TODO: Test a lot of these, currently just the default from the tutorial
        self.depths = [0, 2]#, 4, 8]
        self.circuits_per_depth = 5
        self.qubits = ['Q0', 'Q1']
        self.randomizeout = True
        self.sampler = 'edgegrab'
        self.samplerargs = [0.5]
        self.citerations = 20
        self.compiler_args = ()
        self.seed = 2021
        self.verbosity = 0

    def test_design_construction(self):
        num_mp_procs = 4
        
        serial_design = _rb.DirectRBDesign(self.pspec, self.compilations, self.depths, self.circuits_per_depth,
            qubit_labels=self.qubits, sampler=self.sampler, samplerargs=self.samplerargs,
            addlocal=False, lsargs=(), randomizeout=self.randomizeout, cliffordtwirl=True,
            conditionaltwirl=True, citerations=self.citerations, compilerargs=self.compiler_args,
            partitioned=False, seed=self.seed, verbosity=self.verbosity, num_processes=1)
        
        # Test parallel circuit generation works and is seeded properly
        mp_design = _rb.DirectRBDesign(self.pspec, self.compilations, self.depths, self.circuits_per_depth,
            qubit_labels=self.qubits, sampler=self.sampler, samplerargs=self.samplerargs,
            addlocal=False, lsargs=(), randomizeout=self.randomizeout, cliffordtwirl=True,
            conditionaltwirl=True, citerations=self.citerations, compilerargs=self.compiler_args,
            partitioned=False, seed=self.seed, verbosity=self.verbosity, num_processes=num_mp_procs)

        
        tmodel = pygsti.models.create_crosstalk_free_model(self.pspec)

        [[self.assertAlmostEqual(c.simulate(tmodel)[bs],1.) for c, bs in zip(cl, bsl)] for cl, bsl in zip(mp_design.circuit_lists, mp_design.idealout_lists)]
        
        # for sd_circ, md_circ in zip(serial_design.all_circuits_needing_data, mp_design.all_circuits_needing_data):
        #     if str(sd_circ) != str(md_circ): print('MISMATCH!')
        #     print('  Serial circuit:   ' + str(sd_circ))
        #     print('  Parallel circuit: ' + str(md_circ))
        #     print()

        #Print more debugging info since this test can fail randomly but we can't reproduce this.
        unequal_circuits = []
        for i, (sd, md) in enumerate(zip(serial_design.all_circuits_needing_data,
                                         mp_design.all_circuits_needing_data)):
            if str(sd) != str(md):
                unequal_circuits.append((i, sd, md))
        if len(unequal_circuits) > 0:
            print("%d unequal circuits!!" % len(unequal_circuits))
            print("Seed = ",self.seed, " depths=", self.depths, " circuits_per_depth=", self.circuits_per_depth)
            for i, sd, md in unequal_circuits:
                print("Index: ", i)
                print("Serial design: ", sd.str)
                print("Parall design: ", md.str)
                print()

        self.assertTrue(all([str(sd) == str(md) for sd, md in zip(serial_design.all_circuits_needing_data,
                                                                  mp_design.all_circuits_needing_data)]))


class TestMirrorRBDesign(BaseCase):

    def setUp(self):
        self.num_qubits = 2
        self.qubit_labels = ['Q'+str(i) for i in range(self.num_qubits)]

        gate_names = ['Gi', 'Gxpi2', 'Gxpi', 'Gxmpi2', 'Gypi2', 'Gypi', 'Gympi2', 'Gzpi2', 'Gzpi', 'Gzmpi2', 'Gcphase'] 
        availability = {'Gcphase':[('Q'+str(i),'Q'+str((i+1) % self.num_qubits)) for i in range(self.num_qubits)]}

        self.pspec = pygsti.processors.QubitProcessorSpec(self.num_qubits, gate_names, availability=availability,
                                                          qubit_labels=self.qubit_labels, geometry='line')
        self.clifford_compilations = {
            'absolute': CCR.create_standard(self.pspec, 'absolute', ('paulis', '1Qcliffords'), verbosity=0)
            # SS: I think this is for speed, don't need paulieq for MirrorRB?
        }

        # TODO: Test a lot of these, currently just the default from the tutorial
        self.depths = [0, 2]
        self.circuits_per_depth = 5
        self.qubits = ['Q0', 'Q1']
        self.circuit_type = 'clifford'
        self.sampler = 'edgegrab'
        self.samplerargs = [0.5]
        self.seed = 2021
        self.verbosity = 0

    def test_design_construction(self):
        num_mp_procs = 4
        
        serial_design = _rb.MirrorRBDesign(self.pspec, self.depths, self.circuits_per_depth,
            qubit_labels=self.qubits, circuit_type=self.circuit_type, clifford_compilations=self.clifford_compilations,
            sampler=self.sampler, samplerargs=self.samplerargs,
            localclifford=True, paulirandomize=True, seed=self.seed, verbosity=self.verbosity,
            num_processes=1)
        
        # Test parallel circuit generation works and is seeded properly
        mp_design = _rb.MirrorRBDesign(self.pspec, self.depths, self.circuits_per_depth,
            qubit_labels=self.qubits, circuit_type=self.circuit_type, clifford_compilations=self.clifford_compilations,
            sampler=self.sampler, samplerargs=self.samplerargs,
            localclifford=True, paulirandomize=True, seed=self.seed, verbosity=self.verbosity,
            num_processes=num_mp_procs)

        # for sd_circ, md_circ in zip(serial_design.all_circuits_needing_data, mp_design.all_circuits_needing_data):
        #     if str(sd_circ) != str(md_circ): print('MISMATCH!')
        #     print('  Serial circuit:   ' + str(sd_circ))
        #     print('  Parallel circuit: ' + str(md_circ))
        #     print()
            
        self.assertTrue(all([str(sd) == str(md) for sd, md in zip(serial_design.all_circuits_needing_data,
                                                        mp_design.all_circuits_needing_data)]))


    def test_clifford_design_construction(self):

        n = 2
        qs = ['Q'+str(i) for i in range(n)]
        ring = [('Q'+str(i),'Q'+str(i+1)) for i in range(n-1)]

        gateset1 = ['Gcphase'] + ['Gc'+str(i) for i in range(24)]
        pspec1 = QPS(n, gateset1, availability={'Gcphase':ring}, qubit_labels=qs)
        tmodel1 = pygsti.models.create_crosstalk_free_model(pspec1)

        depths = [0, 2, 8]
        q_set = ('Q0', 'Q1')

        clifford_compilations = {'absolute': CCR.create_standard(pspec1, 'absolute', ('paulis', '1Qcliffords'), verbosity=0)}

        design1 = pygsti.protocols.MirrorRBDesign(pspec1, depths, 3, qubit_labels=q_set, circuit_type='clifford',
                                        clifford_compilations=clifford_compilations, sampler='edgegrab', samplerargs=(0.25,),
                                        localclifford=True, paulirandomize=True, descriptor='A mirror RB experiment',
                                        add_default_protocol=False, seed=None, num_processes=1, verbosity=0)

        [[self.assertAlmostEqual(c.simulate(tmodel1)[bs],1.) for c, bs in zip(cl, bsl)] for cl, bsl in zip(design1.circuit_lists, design1.idealout_lists)]

    def test_nonclifford_design_type1_construction(self):

        n = 2
        qs = ['Q'+str(i) for i in range(n)]
        ring = [('Q'+str(i),'Q'+str(i+1)) for i in range(n-1)]

        gateset2 = ['Gcphase'] + ['Gxpi2', 'Gzr']
        pspec2 = QPS(n, gateset2, availability={'Gcphase':ring}, qubit_labels=qs)
        tmodel2 = pygsti.models.create_crosstalk_free_model(pspec2)

        depths = [0, 2, 8]
        q_set = ('Q0', 'Q1')


        design2 = pygsti.protocols.MirrorRBDesign(pspec2, depths, 3, qubit_labels=q_set, circuit_type='clifford+zxzxz-haar',
                                       clifford_compilations=None, sampler='edgegrab', samplerargs=(0.25,),
                                       localclifford=True, paulirandomize=True, descriptor='A mirror RB experiment',
                                       add_default_protocol=False, seed=None, num_processes=1, verbosity=0)


        [[self.assertAlmostEqual(c.simulate(tmodel2)[bs],1.) for c, bs in zip(cl, bsl)] for cl, bsl in zip(design2.circuit_lists, design2.idealout_lists)]
 
    def test_nonclifford_design_type2_construction(self):

        n = 2
        qs = ['Q'+str(i) for i in range(n)]
        ring = [('Q'+str(i),'Q'+str(i+1)) for i in range(n-1)]

        gateset3 = ['Gczr'] + ['Gxpi2', 'Gzr']
        pspec3 = QPS(n, gateset3, availability={'Gczr':ring}, qubit_labels=qs)
        tmodel3 = pygsti.models.create_crosstalk_free_model(pspec3)

        depths = [0, 2, 8]
        q_set = ('Q0', 'Q1')

        
        design3 = pygsti.protocols.MirrorRBDesign(pspec3, depths, 3, qubit_labels=q_set, circuit_type='cz(theta)+zxzxz-haar',
                                       clifford_compilations=None, sampler='edgegrab', samplerargs=(0.25,),
                                       localclifford=True, paulirandomize=True, descriptor='A mirror RB experiment',
                                       add_default_protocol=False, seed=None, num_processes=1, verbosity=0)


        [[self.assertAlmostEqual(c.simulate(tmodel3)[bs],1.) for c, bs in zip(cl, bsl)] for cl, bsl in zip(design3.circuit_lists, design3.idealout_lists)]

class TestBiRBDesign(BaseCase):

    def setUp(self):
        self.num_qubits = 2
        self.qubit_labels = ['Q'+str(i) for i in range(self.num_qubits)]

        gate_names = ['Gi', 'Gxpi2', 'Gxpi', 'Gxmpi2', 'Gypi2', 'Gypi', 'Gympi2', 'Gzpi2', 'Gzpi', 'Gzmpi2', 'Gcphase'] 
        availability = {'Gcphase':[('Q'+str(i),'Q'+str((i+1) % self.num_qubits)) for i in range(self.num_qubits)]}

        self.pspec = pygsti.processors.QubitProcessorSpec(self.num_qubits, gate_names, availability=availability,
                                                          qubit_labels=self.qubit_labels)
        self.clifford_compilations = CCR.create_standard(self.pspec, 'absolute', ('paulis', '1Qcliffords'), verbosity=0)

        # TODO: Test a lot of these, currently just the default from the tutorial
        self.depths = [0, 2, 4]
        self.circuits_per_depth = 5
        self.qubits = ['Q0', 'Q1']
        self.circuit_type = 'clifford'
        self.sampler = 'edgegrab'
        self.samplerargs = [0.5]
        self.seed = 2021
        self.verbosity = 0

    def test_birb_design_construction_mixed1q2q(self):

        design = pygsti.protocols.BinaryRBDesign(self.pspec, self.clifford_compilations, self.depths, 
                                                 self.circuits_per_depth, qubit_labels=self.qubits, layer_sampling='mixed1q2q',
                                                 sampler=self.sampler, samplerargs=self.samplerargs, 
                                                 seed=self.seed, verbosity=0)
        
    def test_birb_design_construction_alternating1q2q(self):

        design = pygsti.protocols.BinaryRBDesign(self.pspec, self.clifford_compilations, self.depths, 
                                                 self.circuits_per_depth, qubit_labels=self.qubits, layer_sampling='alternating1q2q',
                                                 sampler=self.sampler, samplerargs=self.samplerargs, 
                                                 seed=self.seed, verbosity=0)
        
class TestBiRBProtocol(BaseCase):
    def setUp(self):
        self.num_qubits = 2
        self.qubit_labels = ['Q'+str(i) for i in range(self.num_qubits)]

        gate_names = ['Gi', 'Gxpi2', 'Gxpi', 'Gxmpi2', 'Gypi2', 'Gypi', 'Gympi2', 'Gzpi2', 'Gzpi', 'Gzmpi2', 'Gcphase'] 
        availability = {'Gcphase':[('Q'+str(i),'Q'+str((i+1) % self.num_qubits)) for i in range(self.num_qubits)]}

        self.pspec = pygsti.processors.QubitProcessorSpec(self.num_qubits, gate_names, availability=availability,
                                                          qubit_labels=self.qubit_labels)
        self.clifford_compilations = CCR.create_standard(self.pspec, 'absolute', ('paulis', '1Qcliffords'), verbosity=0)

        # TODO: Test a lot of these, currently just the default from the tutorial
        self.depths = [0, 2, 4]
        self.circuits_per_depth = 5
        self.qubits = ['Q0', 'Q1']
        self.circuit_type = 'clifford'
        self.sampler = 'edgegrab'
        self.samplerargs = [0.5]
        self.seed = 2021
        self.verbosity = 0

        self.design = pygsti.protocols.BinaryRBDesign(self.pspec, self.clifford_compilations, self.depths, 
                                                      self.circuits_per_depth, qubit_labels=self.qubits, layer_sampling='mixed1q2q',
                                                      sampler=self.sampler, samplerargs=self.samplerargs, 
                                                      seed=self.seed, verbosity=0)
        
        self.target_model =  pygsti.models.create_crosstalk_free_model(self.pspec)
        self.noisy_model =  pygsti.models.create_crosstalk_free_model(self.pspec, depolarization_strengths={name: .01 for name in gate_names})

        self.ds = pygsti.data.datasetconstruction.simulate_data(self.target_model, self.design.all_circuits_needing_data, 
                                                                num_samples = 100, seed= self.seed)
        self.ds_noisy = pygsti.data.datasetconstruction.simulate_data(self.noisy_model, self.design.all_circuits_needing_data, 
                                                                num_samples = 100, seed=self.seed)
        
        self.data = pygsti.protocols.ProtocolData(self.design, self.ds)
        self.data_noisy = pygsti.protocols.ProtocolData(self.design, self.ds_noisy)
        
    def test_birb_protocol_ideal(self):
        proto = pygsti.protocols.rb.RandomizedBenchmarking(datatype='energies', defaultfit='A-fixed', rtype='EI',
                 seed=(0.8, 0.95), bootstrap_samples=200, depths='all', square_mean_root=False, name=None)
        
        result = proto.run(self.data)
        self.assertTrue(abs(result.fits['A-fixed'].estimates['r'])<=3e-5)
        
    def test_birb_protocol_noisy(self):
        proto = pygsti.protocols.rb.RandomizedBenchmarking(datatype='energies', defaultfit='A-fixed', rtype='EI',
                 seed=(0.8, 0.95), bootstrap_samples=200, depths='all', square_mean_root=False, name=None)
        
        result = proto.run(self.data_noisy)


class TestCliffordRBProtocol(BaseCase):
    def setUp(self):
        self.num_qubits = 2
        self.qubit_labels = ['Q'+str(i) for i in range(self.num_qubits)]
        
        gate_names = ['Gxpi2', 'Gxmpi2', 'Gypi2', 'Gympi2', 'Gcphase']
        availability = {'Gcphase':[('Q'+str(i),'Q'+str((i+1) % self.num_qubits)) for i in range(self.num_qubits)]}

        self.pspec = pygsti.processors.QubitProcessorSpec(self.num_qubits, gate_names, availability=availability,
                                                          qubit_labels=self.qubit_labels)
        self.compilations = {
            'absolute': CCR.create_standard(self.pspec, 'absolute', ('paulis', '1Qcliffords'), verbosity=0),
            'paulieq': CCR.create_standard(self.pspec, 'paulieq', ('1Qcliffords', 'allcnots'), verbosity=0)
        }

        # TODO: Test a lot of these, currently just the default from the tutorial
        self.depths = [0, 2, 8]
        self.circuits_per_depth = 5
        self.qubits = ['Q0', 'Q1']
        self.citerations = 20
        self.randomizeout = True
        self.interleaved_circuit = None
        self.compiler_args = ()
        self.seed = 2021
        self.verbosity = 0

        self.design = _rb.CliffordRBDesign(self.pspec, self.compilations, self.depths, self.circuits_per_depth, qubit_labels=self.qubits,
                                           randomizeout=self.randomizeout, interleaved_circuit=self.interleaved_circuit,
                                           citerations=self.citerations, compilerargs=self.compiler_args, seed=self.seed,
                                           verbosity=self.verbosity, num_processes=1)
        
        self.target_model =  pygsti.models.create_crosstalk_free_model(self.pspec)
        self.noisy_model =  pygsti.models.create_crosstalk_free_model(self.pspec, depolarization_strengths={name: .01 for name in gate_names})

        self.ds = pygsti.data.datasetconstruction.simulate_data(self.target_model, self.design.all_circuits_needing_data, 
                                                                num_samples = 100, seed=self.seed)
        self.ds_noisy = pygsti.data.datasetconstruction.simulate_data(self.noisy_model, self.design.all_circuits_needing_data, 
                                                                num_samples = 100, seed=self.seed)
        
        self.data = pygsti.protocols.ProtocolData(self.design, self.ds)
        self.data_noisy = pygsti.protocols.ProtocolData(self.design, self.ds_noisy)
        
    def test_cliffordrb_protocol_ideal(self):
        proto = pygsti.protocols.rb.RandomizedBenchmarking(datatype='success_probabilities', defaultfit='A-fixed', rtype='EI',
                 seed=(0.8, 0.95), bootstrap_samples=200, depths='all', square_mean_root=False, name=None)
        
        result = proto.run(self.data)

        self.assertTrue(abs(result.fits['A-fixed'].estimates['r'])<=3e-5)
        
    def test_cliffordrb_protocol_noisy(self):
        proto = pygsti.protocols.rb.RandomizedBenchmarking(datatype='success_probabilities', defaultfit='A-fixed', rtype='EI',
                 seed=(0.8, 0.95), bootstrap_samples=200, depths='all', square_mean_root=False, name=None)
        
        result = proto.run(self.data_noisy)

class TestDirectRBProtocol(BaseCase):
    def setUp(self):
        self.num_qubits = 2
        self.qubit_labels = ['Q'+str(i) for i in range(self.num_qubits)]
        
        gate_names = ['Gxpi2', 'Gxmpi2', 'Gypi2', 'Gympi2', 'Gcphase']
        availability = {'Gcphase':[('Q'+str(i),'Q'+str((i+1) % self.num_qubits)) for i in range(self.num_qubits)]}

        self.pspec = pygsti.processors.QubitProcessorSpec(self.num_qubits, gate_names, availability=availability,
                                                          qubit_labels=self.qubit_labels, geometry='line')
        self.compilations = {
            'absolute': CCR.create_standard(self.pspec, 'absolute', ('paulis', '1Qcliffords'), verbosity=0),
            'paulieq': CCR.create_standard(self.pspec, 'paulieq', ('1Qcliffords', 'allcnots'), verbosity=0)
        }


        # TODO: Test a lot of these, currently just the default from the tutorial
        self.depths = [0, 2, 8]
        self.circuits_per_depth = 5
        self.qubits = ['Q0', 'Q1']
        self.randomizeout = True
        self.sampler = 'edgegrab'
        self.samplerargs = [0.5]
        self.citerations = 20
        self.compiler_args = ()
        self.seed = 2021
        self.verbosity = 0

        self.design =_rb.DirectRBDesign(self.pspec, self.compilations, self.depths, self.circuits_per_depth,
                                        qubit_labels=self.qubits, sampler=self.sampler, samplerargs=self.samplerargs,
                                        addlocal=False, lsargs=(), randomizeout=self.randomizeout, cliffordtwirl=True,
                                        conditionaltwirl=True, citerations=self.citerations, compilerargs=self.compiler_args,
                                        partitioned=False, seed=self.seed, verbosity=self.verbosity, num_processes=1)
                                    
        
        self.target_model =  pygsti.models.create_crosstalk_free_model(self.pspec)
        self.noisy_model =  pygsti.models.create_crosstalk_free_model(self.pspec, depolarization_strengths={name: .01 for name in gate_names})

        self.ds = pygsti.data.datasetconstruction.simulate_data(self.target_model, self.design.all_circuits_needing_data, 
                                                                num_samples = 100, seed=self.seed)
        self.ds_noisy = pygsti.data.datasetconstruction.simulate_data(self.noisy_model, self.design.all_circuits_needing_data, 
                                                                num_samples = 100, seed=self.seed)
        
        self.data = pygsti.protocols.ProtocolData(self.design, self.ds)
        self.data_noisy = pygsti.protocols.ProtocolData(self.design, self.ds_noisy)
        
    def test_directrb_protocol_ideal(self):
        proto = pygsti.protocols.rb.RandomizedBenchmarking(datatype='success_probabilities', defaultfit='A-fixed', rtype='EI',
                 seed=(0.8, 0.95), bootstrap_samples=200, depths='all', square_mean_root=False, name=None)
        
        result = proto.run(self.data)
        self.assertTrue(abs(result.fits['A-fixed'].estimates['r'])<=3e-5)
        
    def test_directrb_protocol_noisy(self):
        proto = pygsti.protocols.rb.RandomizedBenchmarking(datatype='success_probabilities', defaultfit='A-fixed', rtype='EI',
                 seed=(0.8, 0.95), bootstrap_samples=200, depths='all', square_mean_root=False, name=None)
        
        result = proto.run(self.data_noisy)

class TestMirrorRBProtocol(BaseCase):
    def setUp(self):
        self.num_qubits = 2
        self.qubit_labels = ['Q'+str(i) for i in range(self.num_qubits)]

        gate_names = ['Gi', 'Gxpi2', 'Gxpi', 'Gxmpi2', 'Gypi2', 'Gypi', 'Gympi2', 'Gzpi2', 'Gzpi', 'Gzmpi2', 'Gcphase'] 
        availability = {'Gcphase':[('Q'+str(i),'Q'+str((i+1) % self.num_qubits)) for i in range(self.num_qubits)]}

        self.pspec = pygsti.processors.QubitProcessorSpec(self.num_qubits, gate_names, availability=availability,
                                                          qubit_labels=self.qubit_labels, geometry='line')
        self.clifford_compilations = {
            'absolute': CCR.create_standard(self.pspec, 'absolute', ('paulis', '1Qcliffords'), verbosity=0)
            # SS: I think this is for speed, don't need paulieq for MirrorRB?
        }

        # TODO: Test a lot of these, currently just the default from the tutorial
        self.depths = [0, 2, 8]
        self.circuits_per_depth = 5
        self.qubits = ['Q0', 'Q1']
        self.circuit_type = 'clifford'
        self.sampler = 'edgegrab'
        self.samplerargs = [0.5]
        self.seed = 2021
        self.verbosity = 0

        self.design =_rb.MirrorRBDesign(self.pspec, self.depths, self.circuits_per_depth,
                                        qubit_labels=self.qubits, circuit_type=self.circuit_type, clifford_compilations=self.clifford_compilations,
                                        sampler=self.sampler, samplerargs=self.samplerargs,
                                        localclifford=True, paulirandomize=True, seed=self.seed, verbosity=self.verbosity,
                                        num_processes=1)
        
        self.target_model =  pygsti.models.create_crosstalk_free_model(self.pspec)
        self.noisy_model =  pygsti.models.create_crosstalk_free_model(self.pspec, depolarization_strengths={name: .01 for name in gate_names})

        self.ds = pygsti.data.datasetconstruction.simulate_data(self.target_model, self.design.all_circuits_needing_data, 
                                                                num_samples = 100, seed=self.seed)
        self.ds_noisy = pygsti.data.datasetconstruction.simulate_data(self.noisy_model, self.design.all_circuits_needing_data, 
                                                                num_samples = 100, seed=self.seed)
        
        self.data = pygsti.protocols.ProtocolData(self.design, self.ds)
        self.data_noisy = pygsti.protocols.ProtocolData(self.design, self.ds_noisy)
        
    def test_mirrorrb_protocol_ideal(self):
        proto = pygsti.protocols.rb.RandomizedBenchmarking(datatype='adjusted_success_probabilities', defaultfit='A-fixed', rtype='EI',
                 seed=(0.8, 0.95), bootstrap_samples=200, depths='all', square_mean_root=False, name=None)
        
        result = proto.run(self.data)
        self.assertTrue(abs(result.fits['A-fixed'].estimates['r'])<=3e-5)
        
    def test_mirrorrb_protocol_noisy(self):
        proto = pygsti.protocols.rb.RandomizedBenchmarking(datatype='adjusted_success_probabilities', defaultfit='A-fixed', rtype='EI',
                 seed=(0.8, 0.95), bootstrap_samples=200, depths='all', square_mean_root=False, name=None)
        
        result = proto.run(self.data_noisy)
