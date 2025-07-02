from typing import Optional,List
from pydantic import BaseModel, Field

class ValidarLive(BaseModel):
    data:List = Field(...)
    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "telemetria_id":21,
                        "ultimo" :"12:12:12T2024-05-12"
                    },
                    {
                        "telemetria_id":24,
                        "ultimo" :"14:12:12T2024-05-12"
                    }
                ], 
            }
        }

#respuesta cuando todo esta bien
def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

#respuesta cuando algo sale mal 
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


#update_old_salary = (
#"UPDATE contenedores SET ultima_fecha = %s ,set_point = %s ,temp_supply_1= %s ,return_air= %s"
#", ambient_air= %s ,relative_humidity= %s ,avl = %s , defrost_prueba = %s , ripener_prueba = %s , ethylene = %s"
#" , set_point_co2 = %s , co2_reading = %s , humidity_set_point = %s , sp_ethyleno = %s , compress_coil_1 = %s "
#", power_state = %s , evaporation_coil = %s , controlling_mode = %s , stateProcess = %s ,cargo_1_temp = %s "
#", cargo_2_temp = %s , cargo_3_temp = %s , cargo_4_temp = %s , fresh_air_ex_mode = %s  ,imei =%s WHERE estado = 1 AND telemetria_id = %s  ")
#curB.execute(update_old_salary, (trama['fecha'], objetoV['set_point'],objetoV['temp_supply_1'], 
                                    #objetoV['return_air'], objetoV['ambient_air'], objetoV['relative_humidity'], 
                                    #objetoV['avl'], objetoV['inyeccion_pwm'], objetoV['inyeccion_hora'], 
                                    #objetoV['ethylene'], objetoV['set_point_co2'], objetoV['co2_reading'], 
                                    #objetoV['humidity_set_point'], objetoV['sp_ethyleno'],objetoV['compress_coil_1'], 
                                    #objetoV['power_state'],objetoV['evaporation_coil'],objetoV['controlling_mode'],
                                    #objetoV['stateProcess'], objetoV['cargo_1_temp'], objetoV['cargo_2_temp'],
                                    #objetoV['cargo_3_temp'], objetoV['cargo_4_temp'], objetoV['fresh_air_ex_mode'], trama['i'],objetoV['telemetria_id']  ))

class contenedor_base(BaseModel):
    ultima_fecha : Optional[str] | None =None
    fecha : Optional[str] | None =None
    set_point : Optional[float] | None =None
    return_air : Optional[float] | None =None
    temp_supply_1 : Optional[float] | None =None
    ambient_air : Optional[float] | None =None
    relative_humidity : Optional[float] | None =None
    avl : Optional[float] | None =None
    inyeccion_pwm : Optional[float] | None =None
    inyeccion_hora : Optional[float] | None =None
    ethylene : Optional[float] | None =None
    set_point_co2 : Optional[float] | None =None
    co2_reading : Optional[float] | None =None
    humidity_set_point : Optional[float] | None =None
    sp_ethyleno : Optional[float] | None =None
    compress_coil_1 : Optional[float] | None =None
    power_state : Optional[float] | None =None
    evaporation_coil : Optional[float] | None =None
    controlling_mode : Optional[float] | None =None
    
    #stateProcess : Optional[float] | None =None
    stateProcess : Optional[str] | None =None

    cargo_1_temp : Optional[float] | None =None
    cargo_2_temp : Optional[float] | None =None
    cargo_3_temp : Optional[float] | None =None
    cargo_4_temp : Optional[float] | None =None
    fresh_air_ex_mode : Optional[float] | None =None
    telemetria_id : Optional[float] | None =None
    condensation_coil : Optional[float] | None =None
    consumption_ph_1 : Optional[float] | None =None
    consumption_ph_2 : Optional[float] | None =None
    consumption_ph_3 : Optional[float] | None =None
    evaporator_speed : Optional[float] | None =None
    capacity_load : Optional[float] | None =None
    humidity_control : Optional[float] | None =None
    condenser_speed : Optional[float] | None =None
    line_frequency : Optional[float] | None =None
    line_voltage : Optional[float] | None =None
    i : Optional[float] | None =None
    class Config:
        json_schema_extra = {
            "example": {
                "id_evento_telemetria":24,
                "imei_evento_telemetria":"866782042018727",
                "numero_evento_telemetria":"967200500",
                "condicion_evento_telemetria":1,
                "foto_evento_telemetria":"/chip/m2m12.jpg",
                "tipo_evento_telemetria":"ENTEL",
                "observaciones_evento_telemetria":None,

                "token_ztrack":"0f2adb0aee3de894ac4e28bfce85a54f5",
                "estado_evento_telemetria":None,
                "created_at":None,
                "updated_at":None,
                "user_c":0,
                "user_m":None
            }
        }
