import rich
from rich import box
from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table

from textual import events
from textual.app import App
from textual.widget import Widget, Reactive
from textual.widgets import Header, Footer, Placeholder, ScrollView
from textual.views import WindowView

@rich.repr.auto(angular=False)
class PanelWidget(Widget, can_focus=True):

    has_focus: Reactive[bool] = Reactive(False)
    mouse_over: Reactive[bool] = Reactive(False)
    style: Reactive[str] = Reactive("")
    height: Reactive[int | None] = Reactive(None)

    def __init__(self, *, content = None, height: int | None = None):
        super().__init__()
        self.height = height
        self.content = content

    def __rich_repr__(self) -> rich.repr.Result:
        yield "has_focus", self.has_focus, False
        yield "mouse_over", self.mouse_over, False

    def render(self) -> RenderableType:
        return Panel(
            WindowView(widget=Placeholder(name="test")),
            title=self.__class__.__name__,
            border_style="green" if self.mouse_over else "blue",
            box=box.HEAVY if self.has_focus else box.ROUNDED,
            style=self.style,
            height=self.height,
        )

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    async def on_enter(self, event: events.Enter) -> None:
        self.mouse_over = True

    async def on_leave(self, event: events.Leave) -> None:
        self.mouse_over = False


class DuckDash(App):
    async def on_load(self, event: events.Load):
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("q", "quit", "Quit")

    async def on_mount(self):
        """Make a simple grid arrangement."""

        grid = await self.view.dock_grid()
        scroll = ScrollView(gutter=1)
        grid.add_column(fraction=1, name="main", min_size=20)

        grid.add_row(fraction=1, name="header")
        grid.add_row(fraction=4, name="list", min_size=12)
        grid.add_row(fraction=2, name="info", min_size=6)
        grid.add_row(fraction=1, name="footer")

        grid.add_areas(
            area1="main-start|main-end,header",
            area2="main-start|main-end,list",
            area3="main-start|main-end,info",
            area4="main-start|main-end,footer",
        )

        table = Table(title="Demo")
        for i in range(100):
            table.add_row(f"{i}", f"name {i}")
        await scroll.update(table)
        panel = PanelWidget(content="This is the info text")
        header = Header(tall=False)

        grid.place(
            area1=header,
            area2=scroll,
            area3=panel,
            area4=Footer(),
        )


DuckDash.run(title="DuckDash", log="textual.log")
