import argparse
import time

import neuroglancer
import neuroglancer.cli
import cloudvolume
import cloudvolume.server
import imageio
from multiprocessing import Pool
from threading import Thread
from functools import partial


def _cloudvolume_process(cv, cv_link_list, port_list):
    vol = cloudvolume.CloudVolume(cv_link_list[cv])
    hostname = '127.0.0.1'  # 0.0.0.0
    cloudvolume.server.view(vol.cloudpath, hostname=hostname, port=port_list[cv])

class InteractiveInference(object):
    def __init__(self, port, host, cv_list):
        viewer = self.viewer = neuroglancer.Viewer()

        viewer.actions.add('reload-cloudvolume', self._reload_cloudvolume_action)
        with viewer.config_state.txn() as s:
            s.input_event_bindings.data_view['keyr'] = 'reload-cloudvolume'

        self.cv_list = cv_list
        self.cv_num = len(cv_list)
        self.port_list = list(range(port, port + self.cv_num))

        port_num = 0
        with viewer.txn() as s:
            s.layers['unaligned'] = neuroglancer.ImageLayer(
                source='precomputed://' + host + str(self.port_list[port_num]),
                opacity=float(1.0),
            ); port_num += 1
            s.layers['normed'] = neuroglancer.ImageLayer(
                source='precomputed://' + host + str(self.port_list[port_num]),
                opacity=float(1.0),
            ); port_num += 1
            s.layers['normed'].visible = False
            s.layers['aligned_bm'] = neuroglancer.ImageLayer(
                source='precomputed://' + host + str(self.port_list[port_num]),
                opacity=float(1.0),
            ); port_num += 1
            s.layers['aligned_bm'].visible = False
            # s.layers['somas'] = neuroglancer.ImageLayer(
            #     source='precomputed://' + host + str(self.port_list[]),
            #     opacity=float(0.3),
            #     blend='additive',
            #     shader='''
            #         #uicontrol invlerp normalized
            #         void main () {
            #         emitRGB(vec3(0, 0, normalized(getDataValue())));
            #         }
            #     ''',
            # ); port_num += 1
            # s.layers['somas'].visible = False
            # s.layers['aff'] = neuroglancer.ImageLayer(
            #     source='precomputed://' + host + str(self.port_list[1]),
            #     opacity=float(0.5),
            #     shader='''
            #     #uicontrol invlerp red(channel=0)
            #     #uicontrol invlerp green(channel=1)
            #     #uicontrol invlerp blue(channel=2)

            #     void main() {
            #     emitRGB(vec3(red(), green(), blue()));
            #     }
            #     '''
            # ); port_num += 1
            
        # print(cloudvolume.lib.green(host + str(viewer).split(':')[-1]))
        print(cloudvolume.lib.green(str(viewer).split('12345')[-1]))

        self._reload_cloudvolume()

    def _reload_cloudvolume(self):
        try:
            self.pool.terminate()
        except:
            pass
        self.pool = Pool(processes=self.cv_num)
        p_partial = partial(_cloudvolume_process, \
            cv_link_list=cv_list, port_list=self.port_list)
        self.pool.map(p_partial, list(range(self.cv_num)))
        self.pool.close()
        self.pool.join()
    
    def _reload_cloudvolume_action(self, action_state):
        t = Thread(target=self._reload_cloudvolume)
        t.daemon = True
        t.start()


if __name__ == '__main__':
    host = 'http://127.0.0.1:'
    port = 10001
    cv_prefix = 'precomputed://file://'
    cv_list = [
        cv_prefix + '/dc0/CodeReAlign/corgie/tests/img/unaligned',
        cv_prefix + '/dc0/CodeReAlign/corgie/tests/img/img_norm',
        cv_prefix + '/dc0/CodeReAlign/corgie/tests/aligned_blockmatch/img/img_run_x1',
    ]
    
    ap = argparse.ArgumentParser()
    neuroglancer.cli.add_server_arguments(ap)
    neuroglancer.set_server_bind_address(bind_address='127.0.0.1',  # 0.0.0.0
                                         bind_port='12345')

    inf = InteractiveInference(port, host, cv_list)

    while True:
        time.sleep(1000)
