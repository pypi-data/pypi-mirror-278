import pdg

from log_store import log_store

log=log_store.add_logger('scripts:pdg_utils')
#-------------------------------------------------------
def get_bf(decay):
    api    = pdg.connect()
    mother = decay.split('-->')[0].replace(' ', '') 
    for bf in api.get_particle_by_name(mother).exclusive_branching_fractions():
        if bf.is_limit:
            continue

        if bf.description == decay:
            return bf.value

    log.error(f'Cannot find BF for decay: {decay}')
    raise
#-------------------------------------------------------

