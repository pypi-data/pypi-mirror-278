from arcana.core.cli.dataset import add_source, add_sink
from arcana.core.utils.misc import show_cli_trace


def test_add_source_xnat(dataset, cli_runner, arcana_home, work_dir):

    store_nickname = dataset.id + "_store"
    dataset_name = "testing123"
    dataset.store.save(store_nickname)
    dataset_locator = (
        store_nickname + "//" + dataset.id + "@" + dataset_name
    )
    dataset.save(dataset_name)

    result = cli_runner(
        add_source,
        [
            dataset_locator,
            "a_source",
            "text/text-file",
            "--path",
            "file1",
            "--row-frequency",
            "session",
            "--quality",
            "questionable",
            "--order",
            "1",
            "--no-regex",
        ],
    )
    assert result.exit_code == 0, show_cli_trace(result)


def test_add_sink_xnat(dataset, work_dir, arcana_home, cli_runner):

    store_nickname = dataset.id + "_store"
    dataset_name = "testing123"
    dataset.store.save(store_nickname)
    dataset_locator = (
        store_nickname + "//" + dataset.id + "@" + dataset_name
    )
    dataset.save(dataset_name)

    result = cli_runner(
        add_sink,
        [
            dataset_locator,
            "a_sink",
            "text/text-file",
            "--path",
            "deriv",
            "--row-frequency",
            "session",
            "--salience",
            "qa",
        ],
    )
    assert result.exit_code == 0, show_cli_trace(result)
