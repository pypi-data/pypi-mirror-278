from CTADIRAC.Interfaces.API.CTAJob import MetadataDict


software_version = "v0.19.2"

SIMULATION_CONFIG = {
    "ID": 1,
    "input_meta_query": {"parentID": None, "dataset": None},
    "job_config": {
        "type": "MCSimulation",
        "version": "2020-06-29b",
        "array_layout": "Advanced-Baseline",
        "site": "LaPalma",
        "particle": "gamma-diffuse",
        "pointing_dir": "North",
        "zenith_angle": 20,
        "n_shower": 50,
        "magic": None,
        "sct": None,
        "moon": "dark",
        "start_run_number": 0,
    },
}
PROCESSING_CONFIG = {
    "ID": 2,
    "input_meta_query": {"parentID": 1, "moon": "dark"},
    "job_config": {
        "type": "CtapipeProcessing",
        "version": software_version,
        "output_extension": "DL2.h5",
        "options": "--config v3/dl0_to_dl2.yml --config v3/prod5b/subarray_north_alpha.yml",
        "array_layout": "Alpha",
        "data_level": 2,
        "group_size": 1,
    },
}
MERGING_CONFIG_1 = {
    "ID": 3,
    "input_meta_query": {"parentID": 2, "dataset": None},
    "job_config": {
        "type": "Merging",
        "version": software_version,
        "group_size": 5,
        "output_extension": "merged.DL2.h5",
    },
}
MERGING_CONFIG_2 = {
    "ID": 4,
    "input_meta_query": {"parentID": 3, "dataset": None},
    "job_config": {
        "type": "Merging",
        "version": software_version,
        "group_size": 2,
        "output_extension": "alpha_train_en_merged.DL2.h5",
        "options": "--no-dl1-images --no-true-images",
        "catalogs": "DIRACFileCatalog",
    },
}
COMMON_CONFIG = {
    "MCCampaign": "Prod5bTest",
    "configuration_id": 1,
    "base_path": "/vo.cta.in2p3.fr/tests/",
}

WORKFLOW_CONFIG = {
    "ProdSteps": [
        SIMULATION_CONFIG,
        PROCESSING_CONFIG,
        MERGING_CONFIG_1,
        MERGING_CONFIG_2,
    ],
    "Common": COMMON_CONFIG,
}

SIMULATION_OUTPUT_METADATA = MetadataDict(
    [
        ("array_layout", "Advanced-Baseline"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("tel_sim_prog", "sim_telarray"),
        ("tel_sim_prog_version", "2020-06-29b"),
        ("data_level", -1),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
    ]
)

CTAPIPE_PROCESS_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("tel_sim_prog", "sim_telarray"),
        ("tel_sim_prog_version", "2020-06-29b"),
        ("data_level", 2),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
        ("nsb", 1),
        ("type", "CtapipeProcessing"),
        ("version", software_version),
        ("output_extension", "DL2.h5"),
        (
            "options",
            "--config v3/dl0_to_dl2.yml --config v3/prod5b/subarray_north_alpha.yml",
        ),
        ("group_size", 1),
    ]
)

CTAPIPE_PROCESS_OUTPUT_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("analysis_prog", "ctapipe-process"),
        ("analysis_prog_version", software_version),
        ("data_level", 2),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
    ]
)

MERGING1_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("analysis_prog", "ctapipe-process"),
        ("analysis_prog_version", software_version),
        ("data_level", 2),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
        ("nsb", 1),
        ("type", "Merging"),
        ("version", software_version),
        ("group_size", 5),
        ("output_extension", "merged.DL2.h5"),
        ("merged", 0),
    ]
)
MERGING1_OUTPUT_METADATA = MetadataDict(
    [
        ("array_layout", "Alpha"),
        ("site", "LaPalma"),
        ("particle", "gamma-diffuse"),
        ("phiP", 180),
        ("thetaP", 20.0),
        ("sct", "False"),
        ("analysis_prog", "ctapipe-merge"),
        ("analysis_prog_version", software_version),
        ("data_level", 2),
        ("outputType", "Data"),
        ("configuration_id", 1),
        ("MCCampaign", "Prod5bTest"),
        ("merged", 1),
    ]
)
