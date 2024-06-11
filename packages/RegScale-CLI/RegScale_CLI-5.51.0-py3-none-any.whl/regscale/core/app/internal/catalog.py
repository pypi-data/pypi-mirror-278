#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrates catalog export, diagnose and compare into RegScale"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# standard python imports
import click
from rich.console import Console
from rich.progress import Progress

from regscale.core.app.application import Application
from regscale.core.app.utils.catalog_utils.compare_catalog import display_menu as start_compare
from regscale.core.app.utils.catalog_utils.diagnostic_catalog import display_menu as start_diagnostic
from regscale.core.app.utils.catalog_utils.download_catalog import display_menu, select_catalog
from regscale.core.app.utils.catalog_utils.update_catalog_v3 import display_menu as start_update
from regscale.core.app.utils.catalog_utils.update_catalog_v3 import import_catalog
from regscale.core.app.utils.catalog_utils.update_plans import sync_plan_controls, sync_all_plans


@click.group()
def catalog():
    """Export, diagnose, and compare catalog from RegScale.com/regulations."""


@catalog.command(name="sync_security_plans")
@click.option("--all", is_flag=True, help="Flag to sync all System Security Plans.")
@click.option("--plan_id", type=int, help="Sync a specific System Security Plan by ID #.")
@click.option("--dry_run", is_flag=True, help="Perform a dry run of the sync without making any changes.")
def sync_plan(all: bool, plan_id: int, dry_run: bool = False):
    """Sync security plans with the catalog."""
    if all:
        sync_all_plans(dry_run=dry_run)
    elif plan_id:
        sync_plan_controls(ssp_id=plan_id, dry_run=dry_run)
    else:
        click.echo(
            "No valid option provided. Use '--all' to sync all plans or '--plan_id <id>' to sync a specific plan."
        )


@catalog.command(name="import")
@click.option(
    "--catalog_path",
    prompt="Enter the path of the Catalog file to import",
    help="RegScale will load the Catalog",
    type=click.Path(exists=True),
    required=True,
)
def import_(catalog_path: str):
    """Import a catalog.json file into RegScale."""
    console = Console()
    res = import_catalog(Path(catalog_path))
    dat = res.json()
    if dat.get("success"):
        console.print(
            f"Catalog #{dat['catalogId']} imported successfully with {dat['importedItemCount']} " + "controls.",
            style="bold green",
        )
    else:
        console.print(res.json().get("message"), style="bold red")


@catalog.command(name="download")
@click.option("--show_menu", type=bool, default=True, help="Show menu of downloadable catalogs")
@click.option("--select", type=int, help="Select a single catalog to download")
@click.option("--download_all", is_flag=True, help="Download all catalogs")
def export(show_menu: bool, download_all: bool, select: int) -> None:
    """Export catalog from RegScale.com/regulations."""
    app = Application()
    if select or download_all:
        show_menu = False
    max_index = display_menu(show_menu)
    if download_all:
        # Download every URL in the catalog
        cat_range = range(1, max_index + 1)
        downloaded_count = 0
        # use threadpool executor to download all catalogs
        with ThreadPoolExecutor(max_workers=20) as executor:
            args = [(index, False) for index in cat_range]
            with Progress() as progress:
                task = progress.add_task(f"[cyan]Downloading {len(args)} catalogs...", total=len(args))
                for cat, registry_item in executor.map(
                    lambda x: select_catalog(catalog_index=x[0], logging=x[1]), args
                ):
                    if isinstance(cat, dict):
                        downloaded_count += 1
                    else:
                        app.logger.debug(registry_item)
                        app.logger.error(f"Failed to download catalog: {registry_item['title']}")
                    progress.advance(task, 1)
        app.logger.info(f"Successfully Downloaded {downloaded_count} catalogs.")
        return
    if not select:
        select_catalog(catalog_index=0)
    else:
        select_catalog(catalog_index=select)


@catalog.command(name="diagnose")
def diagnostic():
    """Diagnose catalog and output metadata."""
    start_diagnostic()


@catalog.command(name="compare")
def compare():
    """Run diagnostic and compare catalogs while reporting differences."""
    start_compare()


@catalog.command(name="update")
@click.option("--include_meta", is_flag=True, help="Include metadata in the import")
def update(include_meta: bool = False):
    """Update the catalog from RegScale.com/regulations."""
    start_update(include_meta)
