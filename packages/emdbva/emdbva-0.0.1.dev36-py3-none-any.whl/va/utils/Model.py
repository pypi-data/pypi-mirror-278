import os
import sys
from Bio.PDB import MMCIFParser
from Bio.PDB.mmcifio import MMCIFIO
from Bio.PDB.PDBIO import Select
# from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from Bio.PDB.Structure import Structure
import timeit


class NotDisordered(Select):
    """
        Class used to select non-disordered atom from biopython structure instance
    """

    def accept_atom(self, atom):
        """
            Accept only atoms that at "A"
        :param atom: atom instance from biopython library
        :return: True or False
        """
        if (not atom.is_disordered()) or atom.get_altloc() == "A":
            atom.set_altloc(" ")
            return True
        else:
            return False


class Model:
    """
        MapProcessor class contains methods deal with map processing method and model associated map processing methods
        Instance can be initialized with either full map file path or a mrcfile map object
    """

    def __init__(self, input_model, input_dir=None):
        """
            Initialization method with input_model as full path or as a biopython mmcif object and the directory of it
        """
        self.model, self.model_dir = self._set_model_and_dir(input_model) if not input_model else self._set_model_and_dir(input_model, input_dir)

    @staticmethod
    def _set_model_and_dir(input_model, input_dir=None):
        if isinstance(input_model, str) and os.path.isfile(input_model):
            return input_model, os.path.dirname(input_model)
        elif isinstance(input_model, Structure) and input_dir:
            return input_model, input_dir
        else:
            return None, None

    def _structure_to_model(self, pid, cur_model_name):
        """
            Take structure object and output the used model object

        :param pid: String of anything or pdbid
        :param cur_model_name: String of the model name
        :return: TEMPy model instance which will be used for the whole calculation
        """

        p = MMCIFParser()
        io = MMCIFIO()
        org_file_name = cur_model_name
        match_text = 'data_'
        out_moderate_cif = cur_model_name + '_moderated.cif'
        match = self.remove_lines_after_match(cur_model_name, out_moderate_cif, match_text)
        if match:
            structure = p.get_structure(pid, out_moderate_cif)
            cur_model_name = out_moderate_cif
        else:
            structure = p.get_structure(pid, cur_model_name)

        if len(structure.get_list()) > 1:
            org_model = cur_model_name + '_org.cif'
            os.rename(cur_model_name, org_model)
            fstructure = structure[0]
            io.set_structure(fstructure)
            io.save(cur_model_name)
            used_frame = p.get_structure('first', cur_model_name)
            print('!!!There are multiple models in the cif file. Here we only use the first for calculation.')
        else:
            used_frame = structure

        # io.set_structure(used_frame)
        if self.has_disorder_atom(used_frame):
            cur_model_name = cur_model_name + '_Alt_A.cif'
            io.set_structure(used_frame)
            print('There are alternative atom in the model here we only use A for calculations and saved as {}'
                  .format(cur_model_name))
            io.save(cur_model_name, select=NotDisordered())
            new_structure = p.get_structure(pid, cur_model_name)
        else:
            new_structure = used_frame

        setattr(new_structure, "filename", org_file_name)
        tmodel = new_structure

        return tmodel

    @staticmethod
    def remove_lines_after_match(input_file, output_file, match_text):
        """
            Remove lines after the match text
        """

        try:
            with open(input_file, 'r') as infile:
                found_second_match = False
                match_count = 0
                content_before_second_match = []

                for line in infile:
                    if line.startswith(match_text):
                        match_count += 1
                        if match_count >= 2:
                            found_second_match = True
                            break
                    content_before_second_match.append(line)

            if found_second_match:
                with open(output_file, 'w') as outfile:
                    outfile.writelines(content_before_second_match)
                return True
            else:
                print('Second match not found in the file.')
                return False

        except FileNotFoundError:
            print(f'Error: Input file "{input_file}" not found.')
            return False
        except Exception as e:
            print(f'An error occurred: {str(e)}')

            return False

    @staticmethod
    def has_disorder_atom(structure):
        """
            Check if the model contains disorder atoms
        """

        ress = structure.get_residues()
        disorder_flag = False
        for res in ress:
            if res.is_disordered() == 1:
                disorder_flag = True
                return disorder_flag
        return disorder_flag

    def read_model_test(self):
        """
            Read models if '-f' argument is used
        """

        start = timeit.default_timer()
        if self.model is not None:
            model_name = self.model
            full_model_name = model_name
            try:
                model_size = os.stat(full_model_name).st_size
                pid = 'id'
                input_model = []
                tmodel = self._structure_to_model(pid, full_model_name)
                input_model.append(tmodel)

                end = timeit.default_timer()
                print('Read model time: %s' % (end - start))
                print('------------------------------------')

                return input_model, pid, model_size
            except:
                print('!!! File: %s does not exist or corrupted: %s!!!' % (full_model_name, sys.exc_info()[1]))
                print('------------------------------------')
                input_model = None

                return input_model
        else:
            print('No model is given.')
            input_model = None

            return input_model


    def final_model(self):
        """
            Get the final biopython model object
        """
        if isinstance(self.model, Structure):
            return self.model
        else:
            return self.read_model_test()

