import dataol

root_dir = r"C:\Users\Administrator\Desktop\nginx\html\download\python\pycharm\aienable\computer vision\sample_test\samples_xml"
basename = "sample"

# TAF = dataool.Transformer_Annotation_Format(root_dir, basename, ".json", ".xml")
# TAF.batch_transform()

# PP = dataool.Pre_Process(root_dir, basename)
# PP.batch_crop()

PA = dataol.Argumentation(root_dir, basename)
PA.batch_widen_elongated_xml()








