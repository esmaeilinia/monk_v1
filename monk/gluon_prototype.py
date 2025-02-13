from gluon.finetune.imports import *
from system.imports import *

from gluon.finetune.level_14_master_main import prototype_master



class prototype(prototype_master):
    @accepts("self", verbose=int, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def __init__(self, verbose=1):
        super().__init__(verbose=verbose);
        self.system_dict["library"] = "Mxnet";
        self.custom_print("Mxnet Version: {}".format(mx.__version__));
        self.custom_print("");


    ###############################################################################################################################################
    @error_checks(None, ["name", ["A-Z", "a-z", "0-9", "-", "_", "."]], ["name", ["A-Z", "a-z", "0-9", "-", "_", "."]], 
        eval_infer=None, resume_train=None, copy_from=None, pseudo_copy_from=None, summary=None, post_trace=True)
    @accepts("self", str, str, eval_infer=bool, resume_train=bool, copy_from=[list, bool], pseudo_copy_from=[list, bool], summary=bool, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Prototype(self, project_name, experiment_name, eval_infer=False, resume_train=False, copy_from=False, pseudo_copy_from=False, summary=False):
        self.set_system_project(project_name);
        self.set_system_experiment(experiment_name, eval_infer=eval_infer, resume_train=resume_train, copy_from=copy_from, 
            pseudo_copy_from=pseudo_copy_from, summary=summary);
        self.custom_print("Experiment Details");
        self.custom_print("    Project: {}".format(self.system_dict["project_name"]));
        self.custom_print("    Experiment: {}".format(self.system_dict["experiment_name"]));
        self.custom_print("    Dir: {}".format(self.system_dict["experiment_dir"]));
        self.custom_print("");
    ###############################################################################################################################################




    ###############################################################################################################################################
    @warning_checks(None, dataset_path=None, path_to_csv=None, delimiter=None,
        model_name=None, freeze_base_network=None, num_epochs=["lt", 100], post_trace=True)
    @error_checks(None, dataset_path=["folder", "r"], path_to_csv=["file", "r"], delimiter=["in", [",", ";", "-", " "]],
        model_name=None, freeze_base_network=None, num_epochs=["gte", 1], post_trace=True)
    @accepts("self", dataset_path=[str, list, bool], path_to_csv=[str, list, bool], delimiter=str, 
        model_name=str, freeze_base_network=bool, num_epochs=int, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Default(self, dataset_path=False, path_to_csv=False, delimiter=",", model_name="resnet18_v1", freeze_base_network=True, num_epochs=10):
        if(self.system_dict["states"]["eval_infer"]):
            self.Dataset_Params(dataset_path=dataset_path, import_as_csv=import_as_csv, path_to_csv=path_to_csv, delimiter=delimiter);
            self.Dataset();
        else:
            input_size=224;
            self.Dataset_Params(dataset_path=dataset_path, path_to_csv=path_to_csv, delimiter=delimiter, 
                split=0.7, input_size=input_size, batch_size=4, shuffle_data=True, num_processors=psutil.cpu_count());

            #train-val
            self.apply_random_horizontal_flip(probability=0.8, train=True, val=True);
            self.apply_normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], train=True, val=True, test=True);
            self.Dataset();

            self.Model_Params(model_name=model_name, freeze_base_network=freeze_base_network, use_gpu=True, use_pretrained=True);
            self.Model();

            model_name = self.system_dict["model"]["params"]["model_name"];
            if("resnet" in model_name or "alexnet" in model_name or "vgg" in model_name or "darknet" in model_name or "xception" in model_name):
                self.optimizer_sgd(0.01);
                if(num_epochs>10):
                    self.lr_step_decrease(max(min(num_epochs//3, 8), 1), gamma=0.1);
                else:
                    self.lr_step_decrease(1, gamma=0.98);
                self.loss_softmax_crossentropy();

            elif("squeezenet1.0" in model_name):
                self.optimizer_sgd(0.04, weight_decay=0.0002);
                self.lr_step_decrease(1, gamma=0.98);
                self.loss_softmax_crossentropy();

            elif("squeezenet1.1" in model_name):
                self.optimizer_sgd(0.001, weight_decay=0.0002);
                self.lr_step_decrease(1, gamma=0.98);
                self.loss_softmax_crossentropy();

            elif("dense" in model_name):
                self.optimizer_sgd(0.01, weight_decay=0.0001);
                if(num_epochs>10):
                    self.lr_multistep_decrease([max(num_epochs//2, 1), max(3*num_epochs//4, 2)]);
                else:
                    self.lr_step_decrease(1, gamma=0.98);
                self.loss_softmax_crossentropy();

            elif("resnext" in model_name or "senet" in model_name):
                self.optimizer_sgd(0.01, weight_decay=0.0001);
                if(num_epochs>10):
                    self.lr_step_decrease(max(num_epochs//3, 1), gamma=0.1);
                else:
                    self.lr_step_decrease(1, gamma=0.98);
                self.loss_softmax_crossentropy();

            elif("mobile" in model_name):
                self.optimizer_sgd(0.01, weight_decay=0.00004, momentum=0.9);
                self.lr_step_decrease(1, gamma=0.97);
                self.loss_softmax_crossentropy();

            elif("inception" in model_name):
                self.optimizer_sgd(0.045, weight_decay=0.0001, momentum=0.9);
                self.lr_step_decrease(1, gamma=0.9);
                self.loss_softmax_crossentropy();

            self.Training_Params(num_epochs=num_epochs, display_progress=True, display_progress_realtime=True, 
            save_intermediate_models=True, intermediate_model_prefix="intermediate_model_", save_training_logs=True);

            self.system_dict["hyper-parameters"]["status"] = True;

            save(self.system_dict);
    ###############################################################################################################################################


    ###############################################################################################################################################
    @accepts("self", post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Summary(self):
        print_summary(self.system_dict["fname_relative"]);
    ###############################################################################################################################################







    ###############################################################################################################################################
    @accepts("self", post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def List_Models(self):
        self.print_list_models();
    ###############################################################################################################################################






    ###############################################################################################################################################
    @accepts("self", post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def List_Layers(self):
        self.print_list_layers();
    ###############################################################################################################################################





    ###############################################################################################################################################
    @accepts("self", post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def List_Activations(self):
        self.print_list_activations();
    ###############################################################################################################################################







    ###############################################################################################################################################
    @accepts("self", post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def List_Losses(self):
        self.print_list_losses();
    ###############################################################################################################################################







    ###############################################################################################################################################
    @accepts("self", post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def List_Optimizers(self):
        self.print_list_optimizers();
    ###############################################################################################################################################







    ###############################################################################################################################################
    @accepts("self", post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def List_Schedulers(self):
        self.print_list_schedulers();
    ###############################################################################################################################################





    ###############################################################################################################################################
    @accepts("self", post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def List_Transforms(self):
        self.print_list_transforms();
    ###############################################################################################################################################




    ###############################################################################################################################################
    @warning_checks(None, None, None, ["lt", 50], num_epochs=["lte", 10], state=None, post_trace=True)
    @error_checks(None, ["name", ["A-Z", "a-z", "0-9", "-", "_", "."]], None, ["gt", 0, "lte", 100], num_epochs=["gt", 0], 
        state=["in", ["keep_all", "keep_none"]], post_trace=True)
    @accepts("self", str, list, [int, float], num_epochs=int, state=str, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Analyse_Learning_Rates(self, analysis_name, lr_list, percent_data, num_epochs=2, state="keep_all"):
        from gluon_prototype import prototype
        
        project = analysis_name;
        self.custom_print("");
        self.custom_print("Running Learning rate analysis");                                        #Change 1
        self.custom_print("Analysis Name      : {}".format(project));
        self.custom_print("");

        for i in range(len(lr_list)):                                                               #Change 2
            gtf_ = prototype(verbose=0);
            self.custom_print("Running experiment : {}/{}".format(i+1, len(lr_list)));              #Change 3

            experiment = "Learning_Rate_" + str(lr_list[i]);                                        #Change 4
            self.custom_print("Experiment name    : {}".format(experiment))
            
            gtf_.Prototype(project, experiment, pseudo_copy_from=[self.system_dict["project_name"], self.system_dict["experiment_name"]]);

            gtf_.Dataset_Percent(percent_data);
            dataset_type = gtf_.system_dict["dataset"]["dataset_type"];
            dataset_train_path = gtf_.system_dict["dataset"]["train_path"];
            dataset_val_path = gtf_.system_dict["dataset"]["val_path"];
            csv_train = gtf_.system_dict["dataset"]["csv_train"];
            csv_val = gtf_.system_dict["dataset"]["csv_val"];
            if(dataset_type=="train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);
            elif(dataset_type=="csv_train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="csv_train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);


            gtf_.update_learning_rate(lr_list[i])                                               #Change 5
            gtf_.Reload();                                                                          #Change 6
            

            
            gtf_.update_num_epochs(num_epochs);
            gtf_.update_display_progress_realtime(False)
            gtf_.update_save_intermediate_models(False); 

            total_time_per_epoch = gtf_.get_training_estimate();
            total_time = total_time_per_epoch*num_epochs;
            if(int(total_time//60) == 0):
                self.custom_print("Estimated time     : {} sec".format(total_time));
            else:
                self.custom_print("Estimated time     : {} min".format(int(total_time//60)+1));

            gtf_.Train();
            self.custom_print("Experiment Complete");
            self.custom_print("\n");
            

        self.custom_print("Comparing Experiments");
        from compare_prototype import compare

        ctf_ = compare(verbose=0);
        ctf_.Comparison("Comparison_" + analysis_name);
        self.custom_print("Comparison ID:      {}".format("Comparison_" + analysis_name));


        training_accuracies = [];
        validation_accuracies = [];
        training_losses = [];
        validation_losses = [];

        tabular_data = [];

        for i in range(len(lr_list)):                                                               #Change 7
            project = analysis_name;
            experiment = "Learning_Rate_" + str(lr_list[i]);                                        #Change 8
            ctf_.Add_Experiment(project, experiment)

            tmp = [];
            tmp.append(experiment);
            training_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_acc_history.npy";
            tmp.append(np.load(training_accuracy_file)[-1]);
            validation_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_acc_history.npy";
            tmp.append(np.load(validation_accuracy_file)[-1]);
            training_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_loss_history.npy";
            tmp.append(np.load(training_loss_file)[-1]);
            validation_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_loss_history.npy";
            tmp.append(np.load(validation_loss_file)[-1]);
            tabular_data.append(tmp)

        
        ctf_.Generate_Statistics();

        self.custom_print("Generated statistics post all epochs");
        self.custom_print(tabulate(tabular_data, headers=['Experiment Name', 'Train Acc', 'Val Acc', 'Train Loss', 'Val Loss'], tablefmt='orgtbl'));
        self.custom_print("");


        
        return_dict = {};
        for i in range(len(tabular_data)):
            return_dict[tabular_data[i][0]] = {};
            return_dict[tabular_data[i][0]]["training_accuracy"] = tabular_data[i][1];
            return_dict[tabular_data[i][0]]["validation_accuracy"] = tabular_data[i][2];
            return_dict[tabular_data[i][0]]["training_loss"] = tabular_data[i][3];
            return_dict[tabular_data[i][0]]["validation_loss"] = tabular_data[i][4];

            fname = self.system_dict["master_systems_dir_relative"] + analysis_name + "/" + tabular_data[i][0] + "/experiment_state.json";
            system_dict = read_json(fname);
            return_dict[tabular_data[i][0]]["training_time"] = system_dict["training"]["outputs"]["training_time"];


        
        if(state=="keep_none"):
            shutil.rmtree(self.system_dict["master_systems_dir_relative"] + analysis_name);

        return return_dict
        
    ###############################################################################################################################################







    ###############################################################################################################################################
    @warning_checks(None, None, None, ["lt", 50], num_epochs=["lte", 10], state=None, post_trace=True)
    @error_checks(None, ["name", ["A-Z", "a-z", "0-9", "-", "_", "."]], None, ["gt", 0, "lte", 100], num_epochs=["gt", 0], 
        state=["in", ["keep_all", "keep_none"]], post_trace=True)
    @accepts("self", str, list, [int, float], num_epochs=int, state=str, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Analyse_Input_Sizes(self, analysis_name, inp_size_list, percent_data, num_epochs=2, state="keep_all"):
        from gluon_prototype import prototype
        
        project = analysis_name;
        self.custom_print("");
        self.custom_print("Running Input Size analysis");                                              #Change 1
        self.custom_print("Analysis Name      : {}".format(project));
        self.custom_print("");

        for i in range(len(inp_size_list)):                                                              #Change 2
            gtf_ = prototype(verbose=0);    
            self.custom_print("Running experiment : {}/{}".format(i+1, len(inp_size_list)));             #Change 3        

            experiment = "Input_Size_" + str(inp_size_list[i]);                                          #Change 4
            self.custom_print("Experiment name    : {}".format(experiment))
            
            gtf_.Prototype(project, experiment, pseudo_copy_from=[self.system_dict["project_name"], self.system_dict["experiment_name"]]);

            gtf_.Dataset_Percent(percent_data);
            dataset_type = gtf_.system_dict["dataset"]["dataset_type"];
            dataset_train_path = gtf_.system_dict["dataset"]["train_path"];
            dataset_val_path = gtf_.system_dict["dataset"]["val_path"];
            csv_train = gtf_.system_dict["dataset"]["csv_train"];
            csv_val = gtf_.system_dict["dataset"]["csv_val"];
            if(dataset_type=="train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);
            elif(dataset_type=="csv_train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="csv_train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);


            gtf_.update_input_size(inp_size_list[i])                                                        #Change 5 
            gtf_.Reload();                                                                                  #Change 6

            gtf_.update_num_epochs(num_epochs);
            gtf_.update_display_progress_realtime(False)
            gtf_.update_save_intermediate_models(False); 

            total_time_per_epoch = gtf_.get_training_estimate();
            total_time = total_time_per_epoch*num_epochs;
            if(int(total_time//60) == 0):
                self.custom_print("Estimated time     : {} sec".format(total_time));
            else:
                self.custom_print("Estimated time     : {} min".format(int(total_time//60)+1));

            gtf_.Train();
            self.custom_print("Experiment Complete");
            self.custom_print("\n");
            

        self.custom_print("Comparing Experiments");
        from compare_prototype import compare

        ctf_ = compare(verbose=0);
        ctf_.Comparison("Comparison_" + analysis_name);
        self.custom_print("Comparison ID:      {}".format("Comparison_" + analysis_name));


        training_accuracies = [];
        validation_accuracies = [];
        training_losses = [];
        validation_losses = [];

        tabular_data = [];

        for i in range(len(inp_size_list)):                                                                  #Change 7
            project = analysis_name;
            experiment = "Input_Size_" + str(inp_size_list[i]);                                              #Change 8
            ctf_.Add_Experiment(project, experiment)

            tmp = [];
            tmp.append(experiment);
            training_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_acc_history.npy";
            tmp.append(np.load(training_accuracy_file)[-1]);
            validation_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_acc_history.npy";
            tmp.append(np.load(validation_accuracy_file)[-1]);
            training_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_loss_history.npy";
            tmp.append(np.load(training_loss_file)[-1]);
            validation_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_loss_history.npy";
            tmp.append(np.load(validation_loss_file)[-1]);
            tabular_data.append(tmp)

        
        ctf_.Generate_Statistics();

        self.custom_print("Generated statistics post all epochs");
        self.custom_print(tabulate(tabular_data, headers=['Experiment Name', 'Train Acc', 'Val Acc', 'Train Loss', 'Val Loss'], tablefmt='orgtbl'));
        self.custom_print("");


        
        return_dict = {};
        for i in range(len(tabular_data)):
            return_dict[tabular_data[i][0]] = {};
            return_dict[tabular_data[i][0]]["training_accuracy"] = tabular_data[i][1];
            return_dict[tabular_data[i][0]]["validation_accuracy"] = tabular_data[i][2];
            return_dict[tabular_data[i][0]]["training_loss"] = tabular_data[i][3];
            return_dict[tabular_data[i][0]]["validation_loss"] = tabular_data[i][4];

            fname = self.system_dict["master_systems_dir_relative"] + analysis_name + "/" + tabular_data[i][0] + "/experiment_state.json";
            system_dict = read_json(fname);
            return_dict[tabular_data[i][0]]["training_time"] = system_dict["training"]["outputs"]["training_time"];


        
        if(state=="keep_none"):
            shutil.rmtree(self.system_dict["master_systems_dir_relative"] + analysis_name);

        return return_dict
        
    ###############################################################################################################################################





    ###############################################################################################################################################
    @warning_checks(None, None, None, ["lt", 50], num_epochs=["lte", 10], state=None, post_trace=True)
    @error_checks(None, ["name", ["A-Z", "a-z", "0-9", "-", "_", "."]], None, ["gt", 0, "lte", 100], num_epochs=["gt", 0], 
        state=["in", ["keep_all", "keep_none"]], post_trace=True)
    @accepts("self", str, list, [int, float], num_epochs=int, state=str, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Analyse_Batch_Sizes(self, analysis_name, batch_size_list, percent_data, num_epochs=2, state="keep_all"):
        from gluon_prototype import prototype
        
        project = analysis_name;
        self.custom_print("");
        self.custom_print("Running Batch Size analysis");                                                #Change 1
        self.custom_print("Analysis Name      : {}".format(project));
        self.custom_print("");

        for i in range(len(batch_size_list)):                                                            #Change 2
            gtf_ = prototype(verbose=0);    
            self.custom_print("Running experiment : {}/{}".format(i+1, len(batch_size_list)));             #Change 3        

            experiment = "Batch_Size_" + str(batch_size_list[i]);                                          #Change 4, 5
            self.custom_print("Experiment name    : {}".format(experiment))
            
            gtf_.Prototype(project, experiment, pseudo_copy_from=[self.system_dict["project_name"], self.system_dict["experiment_name"]]);

            gtf_.Dataset_Percent(percent_data);
            dataset_type = gtf_.system_dict["dataset"]["dataset_type"];
            dataset_train_path = gtf_.system_dict["dataset"]["train_path"];
            dataset_val_path = gtf_.system_dict["dataset"]["val_path"];
            csv_train = gtf_.system_dict["dataset"]["csv_train"];
            csv_val = gtf_.system_dict["dataset"]["csv_val"];
            if(dataset_type=="train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);
            elif(dataset_type=="csv_train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="csv_train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);


            gtf_.update_batch_size(batch_size_list[i])                                                        #Change 6 
            gtf_.Reload();                                                                                  #Change 7

            gtf_.update_num_epochs(num_epochs);
            gtf_.update_display_progress_realtime(False)
            gtf_.update_save_intermediate_models(False); 

            total_time_per_epoch = gtf_.get_training_estimate();
            total_time = total_time_per_epoch*num_epochs;
            if(int(total_time//60) == 0):
                self.custom_print("Estimated time     : {} sec".format(total_time));
            else:
                self.custom_print("Estimated time     : {} min".format(int(total_time//60)+1));

            gtf_.Train();
            self.custom_print("Experiment Complete");
            self.custom_print("\n");
            

        self.custom_print("Comparing Experiments");
        from compare_prototype import compare

        ctf_ = compare(verbose=0);
        ctf_.Comparison("Comparison_" + analysis_name);
        self.custom_print("Comparison ID:      {}".format("Comparison_" + analysis_name));


        training_accuracies = [];
        validation_accuracies = [];
        training_losses = [];
        validation_losses = [];

        tabular_data = [];

        for i in range(len(batch_size_list)):                                                                  #Change 8
            project = analysis_name;
            experiment = "Batch_Size_" + str(batch_size_list[i]);                                              #Change 9, 10
            ctf_.Add_Experiment(project, experiment)

            tmp = [];
            tmp.append(experiment);
            training_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_acc_history.npy";
            tmp.append(np.load(training_accuracy_file)[-1]);
            validation_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_acc_history.npy";
            tmp.append(np.load(validation_accuracy_file)[-1]);
            training_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_loss_history.npy";
            tmp.append(np.load(training_loss_file)[-1]);
            validation_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_loss_history.npy";
            tmp.append(np.load(validation_loss_file)[-1]);
            tabular_data.append(tmp)

        
        ctf_.Generate_Statistics();

        self.custom_print("Generated statistics post all epochs");
        self.custom_print(tabulate(tabular_data, headers=['Experiment Name', 'Train Acc', 'Val Acc', 'Train Loss', 'Val Loss'], tablefmt='orgtbl'));
        self.custom_print("");


        
        return_dict = {};
        for i in range(len(tabular_data)):
            return_dict[tabular_data[i][0]] = {};
            return_dict[tabular_data[i][0]]["training_accuracy"] = tabular_data[i][1];
            return_dict[tabular_data[i][0]]["validation_accuracy"] = tabular_data[i][2];
            return_dict[tabular_data[i][0]]["training_loss"] = tabular_data[i][3];
            return_dict[tabular_data[i][0]]["validation_loss"] = tabular_data[i][4];

            fname = self.system_dict["master_systems_dir_relative"] + analysis_name + "/" + tabular_data[i][0] + "/experiment_state.json";
            system_dict = read_json(fname);
            return_dict[tabular_data[i][0]]["training_time"] = system_dict["training"]["outputs"]["training_time"];


        
        if(state=="keep_none"):
            shutil.rmtree(self.system_dict["master_systems_dir_relative"] + analysis_name);

        return return_dict
        
    ###############################################################################################################################################






    ###############################################################################################################################################
    @warning_checks(None, None, None, ["lt", 50], num_epochs=["lte", 10], state=None, post_trace=True)
    @error_checks(None, ["name", ["A-Z", "a-z", "0-9", "-", "_", "."]], None, ["gt", 0, "lte", 100], num_epochs=["gt", 0], 
        state=["in", ["keep_all", "keep_none"]], post_trace=True)
    @accepts("self", str, list, [int, float], num_epochs=int, state=str, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Analyse_Models(self, analysis_name, model_list, percent_data, num_epochs=2, state="keep_all"):
        from gluon_prototype import prototype
        
        project = analysis_name;
        self.custom_print("");
        self.custom_print("Running Model analysis");                                                #Change 1
        self.custom_print("Analysis Name      : {}".format(project));
        self.custom_print("");

        for i in range(len(model_list)):                                                            #Change 2
            gtf_ = prototype(verbose=0);    
            self.custom_print("Running experiment : {}/{}".format(i+1, len(model_list)));             #Change 3        

            if(model_list[i][1]):
                experiment = "Model_" + str(model_list[i][0]) + "_freeze_base";                        #Change 4, 5
            else:
                experiment = "Model_" + str(model_list[i][0]) + "_unfreeze_base";

            if(model_list[i][2]):
                experiment += "_pretrained";
            else:
                experiment += "_uninitialized";

            self.custom_print("Experiment name    : {}".format(experiment))
            
            gtf_.Prototype(project, experiment, pseudo_copy_from=[self.system_dict["project_name"], self.system_dict["experiment_name"]]);

            gtf_.Dataset_Percent(percent_data);
            dataset_type = gtf_.system_dict["dataset"]["dataset_type"];
            dataset_train_path = gtf_.system_dict["dataset"]["train_path"];
            dataset_val_path = gtf_.system_dict["dataset"]["val_path"];
            csv_train = gtf_.system_dict["dataset"]["csv_train"];
            csv_val = gtf_.system_dict["dataset"]["csv_val"];
            if(dataset_type=="train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);
            elif(dataset_type=="csv_train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="csv_train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);


            gtf_.update_model_name(model_list[i][0])                                                        #Change 6 
            gtf_.update_freeze_base_network(model_list[i][1])
            gtf_.update_use_pretrained(model_list[i][2])
            gtf_.Reload();                                                                                  #Change 7

            gtf_.update_num_epochs(num_epochs);
            gtf_.update_display_progress_realtime(False)
            gtf_.update_save_intermediate_models(False); 

            total_time_per_epoch = gtf_.get_training_estimate();
            total_time = total_time_per_epoch*num_epochs;
            if(int(total_time//60) == 0):
                self.custom_print("Estimated time     : {} sec".format(total_time));
            else:
                self.custom_print("Estimated time     : {} min".format(int(total_time//60)+1));

            gtf_.Train();
            self.custom_print("Experiment Complete");
            self.custom_print("\n");
            

        self.custom_print("Comparing Experiments");
        from compare_prototype import compare

        ctf_ = compare(verbose=0);
        ctf_.Comparison("Comparison_" + analysis_name);
        self.custom_print("Comparison ID:      {}".format("Comparison_" + analysis_name));


        training_accuracies = [];
        validation_accuracies = [];
        training_losses = [];
        validation_losses = [];

        tabular_data = [];

        for i in range(len(model_list)):                                                                  #Change 8
            project = analysis_name;
            if(model_list[i][1]):
                experiment = "Model_" + str(model_list[i][0]) + "_freeze_base";                        #Change 9, 10
            else:
                experiment = "Model_" + str(model_list[i][0]) + "_unfreeze_base";

            if(model_list[i][2]):
                experiment += "_pretrained";
            else:
                experiment += "_uninitialized";

            ctf_.Add_Experiment(project, experiment)

            tmp = [];
            tmp.append(experiment);
            training_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_acc_history.npy";
            tmp.append(np.load(training_accuracy_file)[-1]);
            validation_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_acc_history.npy";
            tmp.append(np.load(validation_accuracy_file)[-1]);
            training_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_loss_history.npy";
            tmp.append(np.load(training_loss_file)[-1]);
            validation_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_loss_history.npy";
            tmp.append(np.load(validation_loss_file)[-1]);
            tabular_data.append(tmp)

        
        ctf_.Generate_Statistics();

        self.custom_print("Generated statistics post all epochs");
        self.custom_print(tabulate(tabular_data, headers=['Experiment Name', 'Train Acc', 'Val Acc', 'Train Loss', 'Val Loss'], tablefmt='orgtbl'));
        self.custom_print("");


        
        return_dict = {};
        for i in range(len(tabular_data)):
            return_dict[tabular_data[i][0]] = {};
            return_dict[tabular_data[i][0]]["training_accuracy"] = tabular_data[i][1];
            return_dict[tabular_data[i][0]]["validation_accuracy"] = tabular_data[i][2];
            return_dict[tabular_data[i][0]]["training_loss"] = tabular_data[i][3];
            return_dict[tabular_data[i][0]]["validation_loss"] = tabular_data[i][4];

            fname = self.system_dict["master_systems_dir_relative"] + analysis_name + "/" + tabular_data[i][0] + "/experiment_state.json";
            system_dict = read_json(fname);
            return_dict[tabular_data[i][0]]["training_time"] = system_dict["training"]["outputs"]["training_time"];


        
        if(state=="keep_none"):
            shutil.rmtree(self.system_dict["master_systems_dir_relative"] + analysis_name);

        return return_dict
        
    ###############################################################################################################################################







    ###############################################################################################################################################
    @warning_checks(None, None, None, ["lt", 50], num_epochs=["lte", 10], state=None, post_trace=True)
    @error_checks(None, ["name", ["A-Z", "a-z", "0-9", "-", "_", "."]], None, ["gt", 0, "lte", 100], num_epochs=["gt", 0], 
        state=["in", ["keep_all", "keep_none"]], post_trace=True)
    @accepts("self", str, list, [int, float], num_epochs=int, state=str, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Analyse_Optimizers(self, analysis_name, optimizer_list, percent_data, num_epochs=2, state="keep_all"):
        from gluon_prototype import prototype
        
        project = analysis_name;
        self.custom_print("");
        self.custom_print("Running Optimizer analysis");                                                #Change 1
        self.custom_print("Analysis Name      : {}".format(project));
        self.custom_print("");

        for i in range(len(optimizer_list)):                                                            #Change 2
            gtf_ = prototype(verbose=0);    
            self.custom_print("Running experiment : {}/{}".format(i+1, len(optimizer_list)));             #Change 3        

            experiment = "Optimizer_" + str(optimizer_list[i]);                                          #Change 4, 5
            self.custom_print("Experiment name    : {}".format(experiment))
            
            gtf_.Prototype(project, experiment, pseudo_copy_from=[self.system_dict["project_name"], self.system_dict["experiment_name"]]);

            gtf_.Dataset_Percent(percent_data);
            dataset_type = gtf_.system_dict["dataset"]["dataset_type"];
            dataset_train_path = gtf_.system_dict["dataset"]["train_path"];
            dataset_val_path = gtf_.system_dict["dataset"]["val_path"];
            csv_train = gtf_.system_dict["dataset"]["csv_train"];
            csv_val = gtf_.system_dict["dataset"]["csv_val"];
            if(dataset_type=="train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);
            elif(dataset_type=="csv_train"):
                gtf_.update_dataset(dataset_path=dataset_train_path, path_to_csv="sampled_dataset_train.csv");
            elif(dataset_type=="csv_train-val"):
                gtf_.update_dataset(dataset_path=[dataset_train_path, dataset_val_path], 
                    path_to_csv=["sampled_dataset_train.csv", "sampled_dataset_val.csv"]);


            lr = gtf_.system_dict["hyper-parameters"]["learning_rate"]                                      #Change 6 
            if(optimizer_list[i] == "sgd"):
                gtf_.optimizer_sgd(lr);
            elif(optimizer_list[i] == "nag"):
                gtf_.optimizer_nag(lr);
            elif(optimizer_list[i] == "rmsprop"):
                gtf_.optimizer_rmsprop(lr);
            elif(optimizer_list[i] == "adam"):
                gtf_.optimizer_adam(lr);
            elif(optimizer_list[i] == "adagrad"):
                gtf_.optimizer_adagrad(lr);
            elif(optimizer_list[i] == "adadelta"):
                gtf_.optimizer_adadelta(lr);
            elif(optimizer_list[i] == "adamax"):
                gtf_.optimizer_adamax(lr);
            elif(optimizer_list[i] == "nadam"):
                gtf_.optimizer_nadam(lr);
            elif(optimizer_list[i] == "signum"):
                gtf_.optimizer_signum(lr);
            elif(optimizer_list[i] == "ftml"):
                gtf_.optimizer_ftml(lr);
                                                      
            gtf_.Reload();                                                                                  #Change 7

            gtf_.update_num_epochs(num_epochs);
            gtf_.update_display_progress_realtime(False)
            gtf_.update_save_intermediate_models(False); 

            total_time_per_epoch = gtf_.get_training_estimate();
            total_time = total_time_per_epoch*num_epochs;
            if(int(total_time//60) == 0):
                self.custom_print("Estimated time     : {} sec".format(total_time));
            else:
                self.custom_print("Estimated time     : {} min".format(int(total_time//60)+1));


            gtf_.Train();
            self.custom_print("Experiment Complete");
            self.custom_print("\n");
            

        self.custom_print("Comparing Experiments");
        from compare_prototype import compare

        ctf_ = compare(verbose=0);
        ctf_.Comparison("Comparison_" + analysis_name);
        self.custom_print("Comparison ID:      {}".format("Comparison_" + analysis_name));


        training_accuracies = [];
        validation_accuracies = [];
        training_losses = [];
        validation_losses = [];

        tabular_data = [];

        for i in range(len(optimizer_list)):                                                                  #Change 8
            project = analysis_name;
            experiment = "Optimizer_" + str(optimizer_list[i]);                                              #Change 9, 10
            ctf_.Add_Experiment(project, experiment)

            tmp = [];
            tmp.append(experiment);
            training_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_acc_history.npy";
            tmp.append(np.load(training_accuracy_file)[-1]);
            validation_accuracy_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_acc_history.npy";
            tmp.append(np.load(validation_accuracy_file)[-1]);
            training_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/train_loss_history.npy";
            tmp.append(np.load(training_loss_file)[-1]);
            validation_loss_file = self.system_dict["master_systems_dir_relative"] + "/" + project + "/" + experiment + "/output/logs/val_loss_history.npy";
            tmp.append(np.load(validation_loss_file)[-1]);
            tabular_data.append(tmp)

        
        ctf_.Generate_Statistics();

        self.custom_print("Generated statistics post all epochs");
        self.custom_print(tabulate(tabular_data, headers=['Experiment Name', 'Train Acc', 'Val Acc', 'Train Loss', 'Val Loss'], tablefmt='orgtbl'));
        self.custom_print("");


        return_dict = {};
        for i in range(len(tabular_data)):
            return_dict[tabular_data[i][0]] = {};
            return_dict[tabular_data[i][0]]["training_accuracy"] = tabular_data[i][1];
            return_dict[tabular_data[i][0]]["validation_accuracy"] = tabular_data[i][2];
            return_dict[tabular_data[i][0]]["training_loss"] = tabular_data[i][3];
            return_dict[tabular_data[i][0]]["validation_loss"] = tabular_data[i][4];

            fname = self.system_dict["master_systems_dir_relative"] + analysis_name + "/" + tabular_data[i][0] + "/experiment_state.json";
            system_dict = read_json(fname);
            return_dict[tabular_data[i][0]]["training_time"] = system_dict["training"]["outputs"]["training_time"];


        
        if(state=="keep_none"):
            shutil.rmtree(self.system_dict["master_systems_dir_relative"] + analysis_name);

        return return_dict
        
    ###############################################################################################################################################