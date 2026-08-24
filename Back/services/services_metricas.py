from sqlalchemy.orm import Session
from Back.repositories.repositories import RepositoryCatalogoProductos, RepositoryOrdenes
from sqlalchemy import func

class ServiceMetricas:
    def __init__(self, db: Session):
        self.db = db
        self.repo_productos = RepositoryCatalogoProductos(db_session=self.db)
        self.repo_ordenes = RepositoryOrdenes(db_session=self.db)

    def obtener_kpis(self):
        metricas = self.repo_ordenes.metricas_ordenes()

        costos = self.repo_ordenes.costos_totales()

        items_cubiertos = self.repo_ordenes.items_cubiertos()

        pedidos_cubiertos = self.repo_ordenes.estatus_pedidos()

        items_faltantes = dict(self.repo_ordenes.items_faltantes())

        kpi_pedidos = metricas[0]
        kpi_adelantos = metricas[1]
        kpi_deudas = metricas[2]
        kpi_utilidad = metricas[5] - costos
        kpi_costos = costos
        kpi_entregados = metricas[3]
        kpi_pendientes = metricas[4]
        kpi_pedidos_cubiertos = {"Pendiente":pedidos_cubiertos[0], "Parcialmente Asignado":pedidos_cubiertos[1],"Asignado":pedidos_cubiertos[2]}
        kpi_items = {"Asignado":items_cubiertos[0],"Pendiente":items_cubiertos[1]}


        kpi_dict = {
            "pedidos":kpi_pedidos,
            "adelantos":kpi_adelantos,
            "deudas":kpi_deudas,
            "utilidad neta":kpi_utilidad,
            "costos":kpi_costos,
            "pedidos entregados":kpi_entregados,
            "pedidos pendientes":kpi_pendientes,
            "Items": kpi_items,
            "Pedidos cubiertos": kpi_pedidos_cubiertos,
            "Items faltantes": items_faltantes}
        return kpi_dict