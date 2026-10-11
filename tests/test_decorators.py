from src.decorators import log


def test_log_no_output_when_no_errors_and_not_called(capsys):
    """Проверка, что без вызова функции ничего не логируется."""

    @log()
    def unused_function():
        return 42

    captured = capsys.readouterr()
    assert captured.out == ""


def test_log_success_to_console(capsys):
    """Проверка логирования успешного выполнения в консоль."""

    @log()
    def my_function(x, y):
        return x + y

    result = my_function(1, 2)

    captured = capsys.readouterr()

    assert result == 3
    assert captured.out == "my_function ok\n"
