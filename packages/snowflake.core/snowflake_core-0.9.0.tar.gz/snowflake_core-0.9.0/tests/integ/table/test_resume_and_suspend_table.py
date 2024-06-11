

def test_resume_and_suspend_cluster(tables, table_handle):
    table_handle.resume_recluster()
    table_handle.suspend_recluster()
