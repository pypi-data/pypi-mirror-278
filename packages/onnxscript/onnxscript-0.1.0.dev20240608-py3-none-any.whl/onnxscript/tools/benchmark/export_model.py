# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# pylint: disable=import-outside-toplevel

import hashlib
import pprint
import textwrap
import time
from typing import Any


def main(args=None):
    import onnxscript.tools.benchmark

    kwargs: dict[str, Any] = onnxscript.tools.benchmark.get_parsed_args(
        "export_model",
        description=textwrap.dedent(
            """Measures the inference time for a particular model.
            This script can be used to quickly evaluate the improvment made by a pattern optimization
            for a particular model.

            Example::

                python -m onnxscript.tools.benchmark.export_model --model phi --device cuda --config large --num_hidden_layers=6 --dtype=float32 --dynamic=0 --verbose=1 --exporter=dynamo
            """
        ),
        repeat=(10, "number of inferences to measure"),
        warmup=(5, "number of inferences to warm"),
        model=("phi", "model to measure, llama, mistral, phi, ..."),
        exporter=("dynamo", "script, dynamo"),
        device=("cpu", "'cpu' or 'cuda'"),
        target_opset=(18, "opset to convert into, use with backend=custom"),
        config=("small", "default, medium, or small to test"),
        verbose=(0, "verbosity"),
        dump_folder=("", "if not empty, dump the model in that folder"),
        dump_ort=(1, "produce the model optimized by onnxruntime"),
        ort_optimize=(1, "enable or disable onnxruntime optimization"),
        dtype=("default", "cast the model and the inputs into this type"),
        dynamic=(0, "use dynamic shapes"),
        num_hidden_layers=(1, "number of hidden layers"),
        with_mask=(1, "with or without mask, dynamo may fail with a mask"),
        optimization=(
            "",
            "optimization scenario, comma separated value, optimize, rewrite, "
            "inline, set of patterns (default, onnxruntime, customops)",
        ),
        implementation=("eager", "eager or sdpa"),
        new_args=args,
    )

    print("-------------------")
    print("[export_model]")
    pprint.pprint(kwargs)
    print("-------------------")

    # Import is delayed so that help is being display faster (without having to import heavy packages).
    import onnxscript.tools
    import onnxscript.tools.transformers_models

    print(
        f"[export_model] create the model and inputs for {kwargs['model']!r} and config {kwargs['config']!r}"
    )
    begin = time.perf_counter()
    model, example_inputs, dynamic_shapes = (
        onnxscript.tools.transformers_models.get_model_and_inputs(
            warmup=kwargs["warmup"],
            repeat=kwargs["repeat"],
            model=kwargs["model"],
            config=kwargs["config"],
            dynamic_shapes=kwargs["dynamic"],
            device=kwargs["device"],
            num_hidden_layers=kwargs["num_hidden_layers"],
            with_mask=kwargs["with_mask"],
            implementation=kwargs["implementation"],
            dtype=kwargs["dtype"],
        )
    )
    print(f"[export_model] model created in {time.perf_counter() - begin}")
    if kwargs["dynamic"]:
        print(f"[export_model] dynamic_shapes={dynamic_shapes}")
    msg = [tuple(i.shape for i in inp) for inp in example_inputs]
    print(f"[export_model] input_shapes={msg}")
    conversion: dict[str, Any] = {}

    if kwargs["exporter"] == "eager":
        print("[export_model] start benchmark")
        begin = time.perf_counter()
        result = onnxscript.tools.benchmark.run_inference(
            model,
            example_inputs,
            warmup=kwargs["warmup"],
            repeat=kwargs["repeat"],
            verbose=kwargs["verbose"],
        )
        print(f"[export_model] benchmark done in {time.perf_counter() - begin}")
    else:
        print(
            f"[export_model] export to onnx with exporter={kwargs['exporter']!r} "
            f"and optimization={kwargs['optimization']!r}"
        )
        begin = time.perf_counter()
        if kwargs["optimization"]:
            m = hashlib.sha256()
            m.update(kwargs["optimization"].encode())
            so = m.hexdigest()[:5]
        else:
            so = ""
        name = "_".join(
            [
                kwargs["model"],
                kwargs["exporter"],
                "dynamic" if kwargs["dynamic"] else "static",
                kwargs["dtype"].replace("float", "fp"),
                kwargs["device"],
                kwargs["config"],
                f"h{kwargs['num_hidden_layers']}",
                so,
            ],
        )
        filename = f"em_{name}.onnx"

        proto = onnxscript.tools.benchmark.common_export(
            model=model,
            inputs=example_inputs[0],
            exporter=kwargs["exporter"],
            target_opset=kwargs["target_opset"],
            folder=kwargs["dump_folder"],
            filename=filename,
            dynamic_shapes=dynamic_shapes if kwargs["dynamic"] else None,
            optimization=kwargs["optimization"],
            verbose=kwargs["verbose"],
            stats=conversion,
        )
        print(f"[export_model] export to onnx done in {time.perf_counter() - begin}")

        result = onnxscript.tools.benchmark.run_onnx_inference(
            proto,
            example_inputs,
            warmup=kwargs["warmup"],
            repeat=kwargs["repeat"],
            verbose=kwargs["verbose"],
            ort_optimize=kwargs["ort_optimize"],
        )

    print("[export_model] end")
    print("------------------------------")
    for k, v in sorted(kwargs.items()):
        print(f":{k},{v};")
    for k, v in sorted(conversion.items()):
        print(f":{k},{v};")
    for k, v in sorted(result.items()):
        print(f":{k},{v};")


if __name__ == "__main__":
    main()
