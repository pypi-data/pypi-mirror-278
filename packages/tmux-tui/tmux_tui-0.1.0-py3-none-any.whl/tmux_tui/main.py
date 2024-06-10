import itertools
import enum
from abc import abstractmethod, ABC
from typing import Callable
from dataclasses import dataclass, field
from typing import Any
import time
from collections import OrderedDict
import os

import pytermgui as ptg
from pytermgui import Container, Label, Splitter, Button, Window, Checkbox
import libtmux
from copy import deepcopy


def macro_time(fmt: str) -> str:
    return time.strftime(fmt)


server = libtmux.Server()


def n_sessions(fmt: str) -> int:
    """Return the number of sessions open."""
    sessions = server.sessions
    return str(len(sessions))


ptg.tim.define("!time", macro_time)
ptg.tim.define("!n_sessions", n_sessions)


container = Container(
    Label("[bold accent]This is my example"),
    Label(""),
    Label("[surface+1 dim italic]It is very cool, you see"),
    Label(""),
    Splitter(
        Label("My first label", parent_align=0),
        Button("Some button", parent_align=2),
    ),
    Splitter(
        Label("My second label"),
        Checkbox(),
    ),
    Label(""),
    Splitter(Label("Left side"), Label("Middle"), Label("Right side")),
    Label(""),
    Button("Submit button"),
)


class Layout(ABC):
    """ABC for Layouts."""

    @abstractmethod
    def format(self, widgets: list[ptg.Widget]) -> list[Splitter]:
        raise NotImplementedError

    @abstractmethod
    def nrows(self, widgets: list[ptg.Widget]) -> int:
        """The number of rows in the resulting grid."""

    @abstractmethod
    def ncols(self, widgets: list[ptg.Widget]) -> int:
        """The number of cols in the resulting grid."""


@dataclass
class ColumnLayout(Layout):
    n_columns: int

    def format(self, widgets: list[ptg.Widget]) -> list[Splitter]:
        return Formatter.into_columns(widgets, self.n_columns)

    def ncols(self, widgets: list[ptg.Widget]) -> int:
        return self.n_columns

    def nrows(self, widgets: list[ptg.Widget]) -> int:
        ecu = len(widgets) // self.n_columns
        if len(widgets) % self.n_columns != 0:
            return ecu + 1
        else:
            return ecu


@dataclass
class RowLayout(Layout):
    n_rows: int

    def format(self, widgets: list[ptg.Widget]) -> list[Splitter]:
        return Formatter.into_rows(widgets, self.n_rows)

    def ncols(self, widgets: list[ptg.Widget]) -> int:
        ecu = len(widgets) // self.n_rows
        if len(widgets) % self.rows != 0:
            return ecu + 1
        else:
            return ecu

    def nrows(self, widgets: list[ptg.Widget]) -> int:
        return self.n_rows


def default_layout() -> Layout:
    return ColumnLayout(1)


@dataclass
class FormattedWindow:
    """Dataclass comprised of a window and a "Format"."""

    window: Window
    init_function: Callable[..., [list[ptg.Widget]]]
    widgets: list[ptg.Widget] | None = None
    layout: Layout = field(default_factory=default_layout)

    def handle_key(self, key: str) -> bool:
        """Return True if this window handled the provided key."""
        w = self.window
        match key:
            case "j":
                if w.selected_index is None:
                    w.select(0)
                elif w.selected_index == 0:
                    w.select(self.n_columns)
                elif w.selected_index + self.n_columns >= len(self.widgets):
                    pass
                else:
                    w.select(w.selected_index + self.n_columns)

            case "k":
                if w.selected_index is None:
                    w.select(0)
                elif w.selected_index == 0:
                    w.select(0)
                elif w.selected_index - self.n_columns < 0:
                    pass
                else:
                    w.select(w.selected_index - (self.n_columns))

            case _:
                return False

        return True

    def populate(self):
        """Populate the window using a layout and an init function."""
        self.widgets = self.init_function()
        for widget in self.layout.format(self.widgets):
            self.window._add_widget(widget)

        self.n_rows = self.layout.nrows(self.widgets)
        self.n_columns = self.layout.ncols(self.widgets)


def get_session_names() -> list[str]:
    return [s.name for s in server.sessions]

    # manager.layout.add_slot("Body")
    # main_window = ptg.Window()
    #
    # def add_label(label_name: str) -> bool:
    #     """Add a slot and a label to our window manager."""
    #     manager.layout.add_slot(label_name)
    #     main_window._add_widget(Container(Label(label_name)))
    #
    # container_sessions = Container(
    #     Label("Number of sessions: [!n_sessions]%c"),
    #     Label("Hi"),
    #     Splitter(Button("hi", onclick=lambda x: add_label("Hi"))),
    #     ptg.Inspector(manager),
    # )
    #
    # main_window._add_widget(container_sessions)
    # manager.add(main_window)

    # main_window = ptg.Window(box="EMPTY")

    # def window_with_label(label: str, title: str = "label") -> Window:
    #     return Window(Container(Label(label)), title=title)
    #
    # def window_with_labels(labels: list[str], title: str = "labels") -> Window:
    #     labels = [Label(label) for label in labels]
    #     return Window(Container(*labels), title=title)
    #
    # manager.layout.add_slot("hi")
    # manager.layout.add_slot("hi")
    # manager.layout.add_slot("hi")
    # manager.layout.add_slot("hi")
    #
    # manager.add(window_with_label("hi"), animate=False)
    # manager.add(window_with_label("h2"), animate=False)
    # manager.add(window_with_labels(["hi", "hi2"]), animate=False)
    #
    # window_names = [list(w.__dict__.keys()) for w in manager._windows]
    # manager.layout.slots
    # manager.add(Window(Container(ptg.Inspector(window_names))))


@dataclass
class WindowsLayout:
    layout: ptg.Layout
    windows: list[Window]


def window_with_label(label: str, title: str = "label") -> Window:
    return Window(Container(Label(label)), title=title)


def window_with_labels(labels: list[str], title: str = "labels") -> Window:
    labels = [Label(label) for label in labels]
    return Window(Container(*labels), title=title)


def container_with_labels(labels: list[str], split: bool = False) -> Container:
    labels = [Label(label) for label in labels]
    if split:
        return Container(Splitter(*labels))
    else:
        return Container(*labels)


def container_with_buttons(labels: list[str], split: bool = False) -> Container:
    buttons = [Button(label) for label in labels]
    if split:
        return Container(Splitter(*buttons), parent_align=0)
    else:
        return Container(*buttons)


class Manager(ptg.WindowManager):
    """Overrides handle key to add our own bind."""

    def __init__(self, key_handler: Callable[[ptg.WindowManager, str], [bool]]):
        super().__init__()
        self.key_handler = lambda key: key_handler(self, key)

    def handle_key(self, key: str) -> bool:
        """Override."""

        key_handled = self.key_handler(key)
        if not key_handled:
            return super().handle_key(key)
        else:
            return True

            return super().handle_key(key)

        return True


def get_current_session() -> libtmux.Session:
    """Get the attached session."""
    attached_server = server.cmd("display-message", "-p", "#S")
    # Now loop through our known sessions
    for session in server.sessions:
        if session.name == attached_server.stdout[0]:
            return session


current_session = get_current_session()
attached_server = server.cmd("display-message", "-p", "#S").stdout


window_names = [w.name for w in current_session.windows]


def get_window_names(fmt: str) -> str:
    return str([w.name for w in current_session.windows])


ptg.tim.define("!windows", get_window_names)


class AbstractContainer(ABC):
    """Abstract class that can be added as a container to our Tmux application."""

    @abstractmethod
    def container(self) -> Container:
        raise NotImplementedError

    @abstractmethod
    def last_container(self) -> Container:
        raise NotImplementedError


class ReactiveContainer(AbstractContainer):
    def __init__(self, default_factory: Callable[..., [Container]]):
        self.default_factory = default_factory
        self._last_container: Container | None = None

    def container(self) -> Container:
        self._last_container = self.default_factory()
        return self._last_container

    def last_container(self) -> Container:
        return self._last_container


class RegularContainer(AbstractContainer):
    def __init__(self, container: Container):
        self._container = container

    def container(self) -> Container:
        return self._container

    def last_container(self) -> Container:
        return self._container


class LayoutOperation(enum.Enum):
    """Enum of different possible operations."""

    ADD_SLOT = 0
    ADD_WINDOW = 1
    REMOVE_SLOT = 2
    REMOVE_WINDOW = 3


@dataclass
class Operation:
    operation_type: LayoutOperation
    name: str


@dataclass
class Formatter:
    """Dataclass that can arrange a list of widgets into a set of predefined formats."""

    widgets: list[ptg.Widget]

    def columns(self, n_columns: int) -> list[Splitter]:
        """Arrange our widgets into n columns."""
        # We'll use a splitter to split up our widgets horizontally
        splitters: list[Splitter] = []
        it = iter(self.widgets)
        while chunk := list(itertools.islice(it, n_columns)):
            splitters.append(Splitter(*chunk))

        return splitters

    def rows(self, n_rows: int) -> list[Splitter]:
        """Arrange our widgets into n rows."""

        splitters: list[Splitter] = []
        it = iter(self.widgets)
        chunk_size = len(self.widgets) // n_rows
        if chunk_size % n_rows != 0:
            chunk_size += 1

        while chunk := list(itertools.islice(it, chunk_size)):
            splitters.append(Splitter(*chunk))

        return splitters

    @staticmethod
    def into_columns(widgets: list[ptg.Widget], n_columns: int) -> list[Splitter]:
        f = Formatter(widgets)
        return f.columns(n_columns)

    @staticmethod
    def into_rows(widgets: list[ptg.Widget], n_rows: int) -> list[Splitter]:
        f = Formatter(widgets)
        return f.rows(n_rows)


VISION_SERVIES = {
    "llm2sql",
    "sqlbuilder",
    "airbyte",
    "viewcreator",
    "viewserving",
    "viewmonitor",
    "schema-reflector",
}


@dataclass
class Context:
    """A snapshot of windows and slots."""

    slots: OrderedDict[str, ptg.window_manager.layouts.Slot]
    windows: OrderedDict[str, Window]
    active_windows: set[str]
    window_containers: OrderedDict[str, list[AbstractContainer]]
    history: list[Operation]
    formatted_windows: OrderedDict[str, FormattedWindow]


class TmuxApplication:
    def __init__(self):
        self.slots: OrderedDict[str, Any] = OrderedDict()
        self.windows: OrderedDict[str, Window] = OrderedDict()
        self.active_windows: set[str] = set()
        self.window_containers: OrderedDict[str, list[AbstractContainer]] = (
            OrderedDict()
        )
        self.history: list[Operation] = []
        self.formatted_windows: OrderedDict[str, FormattedWindow] = OrderedDict()

        def key_handler(manager: ptg.WindowManager, key: str) -> bool:
            # First and foremost let's get the active window!
            focused_window = self.focused_window()

            if isinstance(focused_window, FormattedWindow):
                if focused_window.handle_key(key):
                    return True

            match key:
                case "d":
                    try:
                        if self.windows.get("main").has_focus:
                            current_session.kill_window(current_session.windows[-1].id)
                            self.refresh_window("tmux")
                            self.refresh_window("main")
                            return True
                    except Exception:
                        pass

                case "a":
                    try:
                        if self.windows.get("main").has_focus:
                            current_session.new_window()
                            self.refresh_window("tmux")
                            self.refresh_window("main")
                            return True
                    except Exception:
                        pass

                case "q":
                    manager.stop()
                    return False
                case "J":
                    manager.focus_next()
                case "K":
                    try:
                        manager.focus_next(step=-1)
                    except Exception:
                        pass
                        # manager.focus_next(step=len(manager._windows))
                case "M":
                    try:
                        manager.focus(self.windows["main"])
                    except Exception:
                        pass
                case "I":
                    try:
                        manager.focus(self.windows["inspect"])
                    except Exception:
                        pass
                case "l":
                    focused_window = manager.focused
                    try:
                        if not focused_window.selected_index:
                            focused_window.select(1)
                            focused_window.selected_index = 1
                        else:
                            focused_window.select(focused_window.selected_index + 1)
                    except Exception:
                        pass
                case "C":
                    self.remove_all()

                case "h":
                    focused_window = manager.focused
                    if not focused_window.selected_index:
                        focused_window.select(0)
                        focused_window.selected_index = 0
                    else:
                        focused_window.select(focused_window.selected_index - 1)

                case _:
                    return False
            return True

        self.manager = Manager(key_handler=key_handler)

    def save_context(self) -> Context:
        """Save a snapshot of this window manager's windows."""
        return Context(
            slots=deepcopy(self.slots),
            windows=deepcopy(self.windows),
            active_windows=deepcopy(self.active_windows),
            window_containers=deepcopy(self.window_containers),
        )

    def focused_window(self) -> Window | FormattedWindow:
        """Retrieve the active window."""
        for v in self.windows.values():
            if v.has_focus:
                return v

        for v in self.formatted_windows.values():
            if v.window.has_focus:
                return v

    def remove_all(self):
        """Remove all windows and slots from our windows manager."""
        for window in self.windows.values():
            self.manager.remove(window, animate=False)

        for name, slot in self.slots.items():
            self.manager.layout.slots.remove(slot)

    def _add_slot(self, name: str):
        self.slots[name] = self.manager.layout.add_slot(name)
        self.history.append(Operation(LayoutOperation.ADD_SLOT, name))

    def add_select_folder_menu(self):
        window_name = "select_folder"
        #
        dir = "/home/ejovo/Fentech/Vision"
        folder_names = [
            file for file in os.listdir(dir) if os.path.isdir(os.path.join(dir, file))
        ]
        folder_names = sorted([f for f in folder_names if f in VISION_SERVIES])

        def onclick_factory(folder_name: str) -> Callable:
            """Create an onclick function that opens a new tmux window and changes directories to the given vision folder."""

            def onclick(a):
                window = current_session.new_window(folder_name)
                window.cmd("send-keys", f"cd {os.path.join(dir, folder_name)}", "Enter")
                window.cmd("send-keys", "clear", "Enter")
                window.cmd("send-keys", "nvim ./", "Enter")

            return onclick

        buttons = [
            Button(fn, parent_align=0, onclick=onclick_factory(fn))
            for fn in folder_names
        ]
        self.add_formatted_window(
            name=window_name,
            init_function=lambda: buttons,
            layout=ColumnLayout(3),
        )

    def add_window(self, name: str, *items):
        if name not in self.slots:
            self._add_slot(name)
        self.windows[name] = Window(title=name, *items)
        self.manager.add(self.windows[name], animate=False)
        self.history.append(Operation(LayoutOperation.ADD_WINDOW, name))
        self.active_windows.add(name)

    def add_formatted_window(
        self,
        name: str,
        init_function: Callable[..., [list[ptg.Widget]]],
        layout: Layout = default_layout(),
    ):
        if name not in self.slots:
            self._add_slot(name)
        self.formatted_windows[name] = FormattedWindow(
            Window(title=name),
            init_function=init_function,
            layout=layout,
        )
        self.formatted_windows[name].populate()
        self.manager.add(self.formatted_windows[name].window, animate=False)
        self.history.append(Operation(LayoutOperation.ADD_WINDOW, name))
        self.active_windows.add(name)

    def add_inspect(self, pyobject: Any, new_slot: bool = True):
        self.add_window("inspect", ptg.Inspector(pyobject))

    def add_reactive_container(
        self,
        window_name: str,
        initializer: Callable[..., [Container]],
    ):
        rc = ReactiveContainer(initializer)
        self.windows[window_name]._add_widget(rc.container())
        if window_name in self.window_containers:
            self.window_containers[window_name].append(rc)
        else:
            self.window_containers[window_name] = [rc]

    def focus(self, window_name: str):
        focused = self.manager.focused
        if focused:
            focused.blur()
        if window_name in self.windows:
            self.manager.focus(self.windows[window_name])
        else:
            self.manager.focus(self.formatted_windows[window_name].window)

    def add_container(self, window_name: str, container: Container):
        container = RegularContainer(container)
        self.windows[window_name]._add_widget(container.container())
        if window_name in self.window_containers:
            self.window_containers[window_name].append(container)
        else:
            self.window_containers[window_name] = [container]

    def hide_window(self, name: str):
        """Remove window from self.manager but don't delete it from TmuxApplication's dictionary."""
        if name in self.active_windows:
            self.manager.remove(self.windows[name], animate=False)
            self.active_windows.remove(name)
            self.history.append(Operation(LayoutOperation.REMOVE_WINDOW, name))

        return True

    def hide_all(self):
        """Hide all windows"""
        for window_name in self.windows.keys():
            self.hide_window(window_name)

    def n_slots(self) -> int:
        """Return the number of slots available."""
        return len(self.slots)

    def n_active_windows(self) -> int:
        """Return the number of active windows."""
        return len(self.active_windows)

    def activate_window(self, name: str):
        if name not in self.active_windows:
            self.manager.add(self.windows[name], assign=name, animate=False)
            self.active_windows.add(name)
            self.history.append(Operation(LayoutOperation.ADD_WINDOW, name))

        return True

    def refresh_window(self, name: str, focus_window_after: str | None = None):
        self.hide_window(name)

        new_containers = [
            container.container() for container in self.window_containers[name]
        ]

        self.windows[name] = Window(title=name)

        for container in new_containers:
            self.windows[name]._add_widget(container)

        self.manager.add(self.windows[name], assign=name, animate=False)
        self.active_windows.add(name)

        if focus_window_after:
            self.focus(focus_window_after)

    def add_main_menu(self):
        self.add_window("main")
        self.add_container(
            window_name="main",
            container=Container(
                Button(
                    "Open Inspect",
                    onclick=lambda x: (
                        self.activate_window("inspect") and self.focus("main")
                    ),
                ),
                Button(
                    "Close Inspect",
                    onclick=lambda x: self.hide_window("inspect")
                    and self.focus("main"),
                ),
                Button("Exit.", onclick=lambda x: self.manager.stop()),
                Label("Num slots: [!n_slots]%c"),
                Label("Num windows: [!n_windows]%c"),
                Button(
                    "Add Tmux Window",
                    onclick=lambda x: (
                        current_session.new_window(),
                        self.refresh_window("tmux"),
                        self.refresh_window("main"),
                    ),
                ),
                Button(
                    "Delete last Tmux Window",
                    onclick=lambda x: (
                        current_session.kill_window(current_session.windows[-1].id),
                        self.refresh_window("tmux"),
                        self.refresh_window("main"),
                    ),
                ),
            ),
        )

    def add_tmux_menu(self):
        def tmux_container() -> Container:
            window_names = [w.name for w in current_session.windows]
            container_sessions = container_with_labels(window_names, split=True)
            container_sessions = container_with_buttons(window_names, split=True)
            return container_sessions

        # First show a list of sessions
        self.add_window("tmux")
        self.add_reactive_container(
            window_name="tmux",
            initializer=tmux_container,
        )

    def main(self):
        """Run the terminal application."""
        with self.manager:
            # self.add_window("slots")
            # self.add_container(
            #     "slots",
            #     Container(Label("N slots: [!n_slots_def]%c")),
            # )
            # self.add_inspect(type(self.slots["slots"]))
            # self.add_inspect(self.history)
            self.add_select_folder_menu()
            self.add_inspect(self.history)
            self.focus("select_folder")


app = TmuxApplication()


# Now I want to be able to create a _window_ that is described using simple parameters


ptg.tim.define("!n_slots", lambda fmt: str(app.n_slots()))
ptg.tim.define("!n_slots_def", lambda fmt: str(len(app.manager.layout.slots)))
ptg.tim.define("!n_windows", lambda fmt: str(app.n_active_windows()))


def main():
    app.main()


if __name__ == "__main__":
    main()
