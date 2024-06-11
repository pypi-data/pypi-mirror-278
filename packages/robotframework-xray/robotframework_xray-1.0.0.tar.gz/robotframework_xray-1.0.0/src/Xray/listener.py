import base64, json, os, platform
import xml.etree.ElementTree as e
from os.path import join
from .xray import Xray
from .config import Config
from bs4 import BeautifulSoup
from robot.libraries.BuiltIn import BuiltIn

class Listener:
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.report = []
        self.suite_index = 0
        self.test_index = 0
        self.keyword_index = 0
        self.pos_test = 0
        self.source = ''
        self.source_kw_index = -1
        self.kw_messages = False
        self.kw_messages_index = -1

    def start_suite(self, name, attrs):
        self.source = attrs['source']
        self.report.append({
            'id': attrs['id'],
            'name': name,
            'longname': attrs['longname'],
            'doc': attrs['doc'],
            'metadata': attrs['metadata'],
            'starttime': attrs['starttime'],
            'tests': [],
            'suites': attrs['suites'],
            'totaltests': attrs['totaltests'],
            'source': attrs['source'],
        })

        self._update_report_file()

    def end_suite(self, name, attrs):
        self.report[self.suite_index]['endtime'] = attrs['endtime']
        self.report[self.suite_index]['elapsedtime'] = attrs['elapsedtime']
        self.report[self.suite_index]['status'] = attrs['status']
        self.report[self.suite_index]['message'] = attrs['message']
        self.report[self.suite_index]['totaltests'] = attrs['totaltests']
        self.report[self.suite_index]['statistics'] = attrs['statistics']

        self.suite_index = self.suite_index + 1
        self.test_index = 0
        self.keyword_index = 0

        self._update_report_file()

    def start_test(self, name, attrs):
        self.report[self.suite_index]['tests'].append({
            'id': attrs['id'],
            'longname': attrs['longname'],
            'doc': attrs['doc'],
            'tags': attrs['tags'],
            'lineno': attrs['lineno'],
            'source': attrs['source'],
            'starttime': attrs['starttime'],
            'template': attrs['template'],
            'originalname': attrs['originalname'],
            'keywords': [],
            'video': '',
        })

        self._update_report_file()

    def end_test(self, name, attrs):
        self.report[self.suite_index]['tests'][self.test_index]['endtime'] = attrs['endtime']
        self.report[self.suite_index]['tests'][self.test_index]['elapsedtime'] = attrs['elapsedtime']
        self.report[self.suite_index]['tests'][self.test_index]['status'] = attrs['status']

        tags = self.report[self.suite_index]['tests'][self.test_index]['tags']
        line_start = self.report[self.suite_index]['tests'][self.test_index]['lineno']
        line_end = self.report[self.suite_index]['tests'][self.test_index]['keywords']
        if line_start <= line_end[-1]['lineno']:
            line_end = line_end[-1]['lineno']
        else:
            line_end = line_end[-2]['lineno']
        line_count = 1
        xrayTestIssueId = ''
        test = '{code}'
        
        file = open(self.source, 'r')
        if tags:
            for line in file:
                if line_count >= line_start and line_count <= line_end:
                    if '[Tags]' in line:
                        test += '\t[Tags]'
                        for tag in self.report[self.suite_index]['tests'][self.test_index]['tags']:
                            if self._has_xray_config() and Config.project_key() in tag:
                                xrayTestIssueId = Xray.getTest(tag)
                                Xray.updateXrayTestType(xrayTestIssueId)
                            test += '\t{}'.format(tag)
                        test += '\n'
                    else:
                        if '#' not in line.strip()[0]:
                            test += line
                line_count += 1
        test += '{code}'
        file.close()

        if xrayTestIssueId:
            self.report[self.suite_index]['tests'][self.test_index]['issueId'] = str(xrayTestIssueId)
            if Config.mode() == 'ALL' or Config.mode() == 'SYNC':
                Xray.updateXrayTest(xrayTestIssueId, test)
                print('\n')
                print('------------------------------------------------------------------------------')
                print(f'Test definition synchronized successfully!')
                print('------------------------------------------------------------------------------')

        self.test_index = self.test_index + 1
        self.keyword_index = 0
        self.source_kw_index = -1

        self._update_report_file()

    def start_keyword(self, name, attrs):
        self._add_keyword(attrs)
        self._update_report_file()

    def end_keyword(self, name, attrs):
        self.keyword_index = self._update_keyword(attrs)
        self._update_report_file()

    def log_message(self, message):
        if message['message'].__contains__('<img'):
            soup = BeautifulSoup(message['message'], 'html.parser')
            image_src = soup.img.get('src')

            if not image_src.__contains__('data:image/png;base64,'):
                with open(join(BuiltIn().get_variable_value('${OUTPUT_DIR}'), image_src), 'rb') as img_file:
                    b64_string = base64.b64encode(img_file.read())
                    message['message'] = '</td></tr><tr><td colspan="3"><img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="{}{}" width="800px"></a>'.format('data:image/png;base64,', b64_string.decode('utf-8'))
        
        if message['message'].__contains__('<source'):
            soup = BeautifulSoup(message['message'], 'html.parser')
            video_src = soup.source.get('src')
            with open(join(BuiltIn().get_variable_value('${OUTPUT_DIR}'), video_src), 'rb') as video_file:
                self.report[self.suite_index]['tests'][self.test_index]['video'] = base64.b64encode(video_file.read()).decode('utf-8')
                message['message'] = 'Attached evidence'

        if self.kw_messages:
            self.report[self.suite_index]['tests'][self.test_index]['keywords'][self.source_kw_index]['keywords'][self.kw_messages_index]['messages'].append({
                'timestamp': message['timestamp'],
                'message': message['message'],
                'level': message['level'],
                'html': message['html'],
            })
        else:
            self.report[self.suite_index]['tests'][self.test_index]['keywords'][self.source_kw_index]['messages'].append({
                'timestamp': message['timestamp'],
                'message': message['message'],
                'level': message['level'],
                'html': message['html'],
            })

        self._update_report_file()

    def close(self):
        self.test_index = 0
        self.keyword_index = 0

        self._update_report_file()

        if self._has_xray_config() and (Config.mode() == 'ALL' or Config.mode() == 'RESULTS'):
            report = e.Element('robot', {
                'os': platform.system(),
                'python': platform.python_version(),
                'rpa': 'true',
                'schemaversion': '3',
            })

            for suite in self.report:
                sub_element_suite = e.SubElement(report, 'suite', {
                    'id': suite.get('id'),
                    'name': suite.get('name'),
                    'source': suite.get('source'),
                })
                
                for test in suite.get('tests'):
                    sub_element_test = e.SubElement(sub_element_suite, 'test', {
                        'id': test.get('id'),
                        'name': test.get('originalname'),
                        'line': str(test.get('lineno')),
                    })

                    if test.get('tags'):
                        sub_element_tag = e.SubElement(sub_element_test, 'tags')
                        for tag in test.get('tags'):
                            e.SubElement(sub_element_tag, 'tag').text = tag

                    for keyword in test.get('keywords'):
                        sub_element_keyword = e.SubElement(sub_element_test, 'kw', {
                            'type': keyword.get('type'),
                            'name': keyword.get('kwname'),
                            'library': keyword.get('library'),
                        })
                        
                        if keyword.get('args'):
                            sub_element_arguments = e.SubElement(sub_element_keyword, 'arguments')
                            for arg in keyword.get('args'):
                                e.SubElement(sub_element_arguments, 'arg').text = arg
                        
                        if keyword.get('doc'):
                            e.SubElement(sub_element_keyword, 'doc').text = keyword.get('doc')

                        if keyword.get('messages'):
                            for message in keyword.get('messages'):
                                e.SubElement(sub_element_keyword, 'msg', {
                                    'timestamp': message.get('timestamp'),
                                    'level': message.get('level'),
                                    'html': message.get('html'),
                                }).text = message.get('message')
                        
                        if keyword.get('status'):
                            e.SubElement(sub_element_keyword, 'status', {
                                'status': keyword.get('status'),
                                'starttime': keyword.get('starttime'),
                                'endtime': keyword.get('endtime'),
                            })

                        for sub_keyword in keyword.get('keywords'):
                            sub_element_keyword_kws = e.SubElement(sub_element_keyword, 'kw', {
                                'type': sub_keyword.get('type'),
                                'name': sub_keyword.get('kwname'),
                                'library': sub_keyword.get('library'),
                            })
                            
                            if sub_keyword.get('args'):
                                sub_element_arguments = e.SubElement(sub_element_keyword_kws, 'arguments')
                                for arg in sub_keyword.get('args'):
                                    e.SubElement(sub_element_arguments, 'arg').text = arg
                            
                            if sub_keyword.get('doc'):
                                e.SubElement(sub_element_keyword_kws, 'doc').text = sub_keyword.get('doc')

                            if sub_keyword.get('messages'):
                                for message in sub_keyword.get('messages'):
                                    e.SubElement(sub_element_keyword_kws, 'msg', {
                                        'timestamp': message.get('timestamp'),
                                        'level': message.get('level'),
                                        'html': message.get('html'),
                                    }).text = message.get('message')
                        
                            if keyword.get('status'):
                                e.SubElement(sub_element_keyword_kws, 'status', {
                                    'status': keyword.get('status'),
                                    'starttime': keyword.get('starttime'),
                                    'endtime': keyword.get('endtime'),
                                })

            e.SubElement(report, 'doc').text = suite.get('doc')
            e.SubElement(report, 'status', {
                'status': suite.get('status'),
                'starttime': suite.get('starttime'),
                'endtime': suite.get('endtime'),
            })

            a = e.ElementTree(report)
            a.write(file_or_filename='report.xml', encoding='UTF-8', xml_declaration=True)

            print('Report is being sent, please wait a moment...')
            testExecutionId = Xray.importExecutionRobot()
            print('Report sent successfully, see more at:\nhttps://atlassian.net/browse/{}'.format(testExecutionId['key']))
            print('------------------------------------------------------------------------------')
            print('Now if there is evidence we will be sending it, wait a moment...')
            self._send_evidence(self.report, testExecutionId['issueId'])
            print('==============================================================================')

    def _send_evidence(self, report, testExecutionId):
        for suite in report:
            for test in suite['tests']:
                test_key = ''
                for tag in test['tags']:
                    if Config.project_key() in tag:
                        test_key = tag
                if test['video'] and test_key:
                    id = Xray.getTestRun(test['issueId'], testExecutionId)
                    Xray.addEvidenceToTestRun(id, 'Evidence_{}.webm'.format(test_key), test['video'])
                    print('- {} test evidence submitted successfully!'.format(test_key))
                else:
                    print('- {} test does not have evidence, skip step...'.format(test_key))
    
    def _add_keyword(self, attrs):
        if self.report[self.suite_index]['tests'][self.test_index]['source'] == attrs['source']:
            self.report[self.suite_index]['tests'][self.test_index]['keywords'].append({
                'doc': attrs['doc'],
                'assign': attrs['assign'],
                'tags': attrs['tags'],
                'lineno': attrs['lineno'],
                'source': attrs['source'],
                'type': attrs['type'],
                'status': attrs['status'],
                'starttime': attrs['starttime'],
                'kwname': attrs['kwname'],
                'library': attrs['libname'],
                'args': attrs['args'],
                'messages': [],
                'keywords': [],
            })

            self.kw_messages = False
            self.source_kw_index = self.source_kw_index + 1
            self.kw_messages_index = -1
        else:
            self.report[self.suite_index]['tests'][self.test_index]['keywords'][self.source_kw_index]['keywords'].append({
                'doc': attrs['doc'],
                'assign': attrs['assign'],
                'tags': attrs['tags'],
                'lineno': attrs['lineno'],
                'source': attrs['source'],
                'type': attrs['type'],
                'status': attrs['status'],
                'starttime': attrs['starttime'],
                'kwname': attrs['kwname'],
                'library': attrs['libname'],
                'args': attrs['args'],
                'messages': [],
                'keywords': [],
            })

            self.kw_messages = True
            self.kw_messages_index = self.kw_messages_index + 1

    def _update_keyword(self, attrs) -> int:
        keyword_pos = 0

        if self.report[self.suite_index]['tests'][self.test_index]['source'] == attrs['source']:
            for kw in self.report[self.suite_index]['tests'][self.test_index]['keywords']:
                if kw['lineno'] == attrs['lineno']:
                    self.report[self.suite_index]['tests'][self.test_index]['keywords'][keyword_pos]['endtime'] = attrs['endtime']
                    self.report[self.suite_index]['tests'][self.test_index]['keywords'][keyword_pos]['elapsedtime'] = attrs['elapsedtime']
                    self.report[self.suite_index]['tests'][self.test_index]['keywords'][keyword_pos]['status'] = attrs['status']
                keyword_pos = keyword_pos + 1
        
        return keyword_pos
    
    def _update_report_file(self):
        with open(join(os.path.abspath(os.curdir), 'report.json'), 'w') as write_report_file:
            json.dump(self.report, write_report_file, indent=4)

    def _has_xray_config(self) -> bool:
        if Config.project_key() and Config.xray_api() and Config.xray_client_id() and Config.xray_client_secret():
            return True
        return False