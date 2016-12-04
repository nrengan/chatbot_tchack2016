from crystal_knows import *
from flask import *
from twilio_helper import send_text
from saltedge_helper import *
from database import *
# from personality_insights import *
# from tone_analyzer import *
from AlchemyLanguageV1 import *
import unicodedata

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')
@app.route('/')
@app.route("/index")
@app.route("/index.html")
def index():
	data = []
	return render_template('/index.html', data = data)

@app.route("/register")
@app.route("/register.html")
def register_page():
	data = []
	return render_template('/register.html', data = data)

@app.route("/login")
@app.route("/login.html")
def login_page():
	id = request.args.get('id')
	record = loadData()
	if id in record :
		text_test("You have login in your bank account!", "+447873124771")
		return json.dumps(record[id])
	else :
		return render_template('/login.html', id = id)

@app.route('/send_text_test')
@app.route('/send_text_test/<string:exNumber>')
def text_test(text="Hi, there!", exNumber="+447873124771"):
    send_text(exNumber, text)
    return "Done"

@app.route('/newCustomer/<string:id>/<string:username>/<string:password>')
def create_new_customer(id="exampleID", username="username", password="password"):
	record = loadData()
	headers = { 'Accept': 'application/json', 'Client-id' : 'UDbWPMg0eJ8-_RlC5k7Thw', 'App-secret' : 'jvcjbJPm9-TUXBRLf3LK6nDgHsiz9xD6yrjJgPYA5Bg', 'Content-Type' : 'application/json' }
	r = get_new_customer(headers, unicodedata.normalize('NFKD', id).encode('ascii','ignore'))
	headers['Customer-secret'] = unicodedata.normalize('NFKD', r['data']['secret']).encode('ascii','ignore')
	r = get_new_login(headers, username, password)
	headers['Login-secret'] = unicodedata.normalize('NFKD', r['data']['secret']).encode('ascii','ignore')
	record[id] = headers
	saveData(record)
	return json.dumps(headers)

@app.route('/newAccount/<string:id>')
def create_new_account(id="exampleID"):
	record = loadData()
	r = get_new_account(record[id])
	return r

@app.route('/newTransactions/<string:id>')
def create_new_transactions(id="exampleID"):
	record = loadData()
	r = get_transactions(record[id])
	return r

@app.route('/loginWithUsername', methods=['POST'])
def login_with_username():
    username = request.form['username']
    password = request.form['password']
    fid = request.form['id']
    headers = create_new_customer(fid, username, password)
    # send request to chatfuel to continue the conversation
    text_test("You have login first time in your bank account!", "+447873124771")
    return headers

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('Webapp', path)

# region "Bot commands"
users = {}
potential_users = {}


@app.route('/linkedin')
def linked_in_check():
    uid = request.args.get('uid')
    if uid not in users:


        pers_details = person_details(person_query(request.args.get('fname'), request.args.get('lname')), 0)

        response = {"messages": [
            {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [{
                            "title": "LinkedIn Connect",
                            "image_url": pers_details['person']['photo_url'],

                        }],
                    },

                }

            },
            {
                "text": "Is this your linkedin profile?",
                "quick_replies": [
                    {"title": "Yes", "block_names": ["linkedin_link"]},
                    {"title": "No", "block_names": ["linkedin_fail"]}
                ]

            }
        ]}
        potential_users[uid] = {'name': request.args.get('fname') + request.args.get('lname'), 'id': uid,
                                'linkedin_details': pers_details['person']}
        return jsonify(**response)
        #               'personality': personality_type(pers_details)}
    else:
        return "You appear to already be connected to LinkedIn"


@app.route('/linkedin_confirm')
def linked_in_confirm():
    uid = request.args.get('uid')
    users[uid] = potential_users[uid]
    response = {"messages": [
        {
            "text": "Awesome, your LinkedIn account has been added, and we'll now tailor responses based on your personality.",
            "quick_replies": [
                {"title": "Continue", "block_names": ["C.5. Psychological profile results"]},
            ]
        }
    ]}

    return jsonify(**response)


@app.route("/generatelink")
def generate_link():
    uid = request.args.get('uid')

    response = {"messages": [
        {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Great, we've generated a custom link for you to log in to your bank's website!",
                    "buttons": [{
                         "type" : "web_url",
                         "url" : "https://2d0158a6.ngrok.io/login?id=" + uid,
                         "title" : "Log in now"
                },],
                },

            }

        }
    ]}
    return jsonify(**response)

# endregion

@app.route('/connecttowatson')
def ConnectToWatson(text=None):
	pi = PersonalityInsights(text)
	ta = ToneAnalize(text)
	al = AlchemyLanguageV1(text)
	return json.dumps({'pi' : pi, 'ta' : ta, 'al' : al})

@app.route('/personalityinsights')
def PersonalityInsights(text=None):
	if text is None :
		text = "Mr. Vice President, my old colleague from Massachusetts and your new Speaker, John McCormack, Members of the 87th Congress, ladies and gentlemen: This week we begin anew our joint and separate efforts to build the American future. But, sadly, we build without a man who linked a long past with the present and looked strongly to the future. Mister Sam Rayburn is gone. Neither this House nor the Nation is the same without him. Members of the Congress, the Constitution makes us not rivals for power but partners for progress. We are all trustees for the American people, custodians of the American heritage. It is my task to report the State of the Union--to improve it is the task of us all. In the past year, I have traveled not only across our own land but to other lands-to the North and the South, and across the seas. And I have found--as I am sure you have, in your travels--that people everywhere, in spite of occasional disappointments, look to us--not to our wealth or power, but to the splendor of our ideals. For our Nation is commissioned by history to be either an observer of freedom's failure or the cause of its success. Our overriding obligation in the months ahead is to fulfill the world's hopes by fulfilling our own faith. 1. STRENGTHENING THE ECONOMY That task must begin at home. For if we cannot fulfill our own ideals here, we cannot expect others to accept them. And when the youngest child alive today has grown to the cares of manhood, our position in the world will be determined first of all by what provisions we make today--for his education, his health, and his opportunities for a good home and a good job and a good life. At home, we began the year in the valley of recession--we completed it on the high road of recovery and growth. With the help of new congressionally approved or administratively increased stimulants to our economy, the number of major surplus labor u areas has declined from 101 to 60; nonagricultural employment has increased by more than a million jobs; and the average factory work-week has risen to well over 40 hours. At year's end the economy which Mr. Khrushchev once called a stumbling horse was racing to new records in consumer spending, labor income, and industrial production. We are gratified--but we are not satisfied. Too many unemployed are still looking for the blessings of prosperity- As those who leave our schools and farms demand new jobs, automation takes old jobs away. To expand our growth and job opportunities, I urge on the Congress three measures:(1) First, the Manpower Training and Development Act, to stop the waste of able-bodied men and women who want to work, but whose only skill has been replaced by a machine, or moved with a mill, or shut down with a mine; (2) Second, the Youth Employment Opportunities Act, to help train and place not only the one million young Americans who are both out of school and out of work, but the twenty-six million young Americans entering the labor market in this decade; and (3) Third, the 8 percent tax credit for investment in machinery and equipment, which, combined with planned revisions of depreciation allowances, will spur our modernization, our growth, and our ability to compete abroad. Moreover--pleasant as it may be to bask in the warmth of recovery--let us not forget that we have suffered three recessions in the last 7 years. The time to repair the roof is when the sun is shining--by filling three basic gaps in our anti-recession protection. We need: (1) First, presidential standby authority, subject to congressional veto, to adjust personal income tax rates downward within a specified range and time, to slow down an economic decline before it has dragged us all down; (2) Second, presidential standby authority, upon a given rise in the rate of unemployment, to accelerate Federal and federally-aided capital improvement programs; and (3) Third, a permanent strengthening of our unemployment compensation system--to maintain for our fellow citizens searching for a job who cannot find it, their purchasing power and their living standards without constant resort--as we have seen in recent years by the Congress and the administrations-to temporary supplements. If we enact this six-part program, we can show the whole world that a free economy need not be an unstable economy--that a free system need not leave men unemployed--and that a free society is not only the most productive but the most stable form of organization yet fashioned by man. II. FIGHTING INFLATION But recession is only one enemy of a free economy--inflation is another. Last year, 1961, despite rising production and demand, consumer prices held almost steady--and wholesale prices declined. This is the best record of overall price stability of any comparable period of recovery since the end of World War II. Inflation too often follows in the shadow of growth--while price stability is made easy by stagnation or controls. But we mean to maintain both stability and growth in a climate of freedom. Our first line of defense against inflation is the good sense and public spirit of business and labor--keeping their total increases in wages and profits in step with productivity. There is no single statistical test to guide each company and each union. But I strongly urge them--for their country's interest, and for their own--to apply the test of the public interest to these transactions. Within this same framework of growth and wage-price stability: --This administration has helped keep our economy competitive by widening the access of small business to credit and Government contracts, and by stepping up the drive against monopoly, price-fixing, and racketeering; --We will submit a Federal Pay Reform bill aimed at giving our classified, postal, and other employees new pay scales more comparable to those of private industry; --We are holding the fiscal 1962 budget deficit far below the level incurred after the last recession in 1958; and, finally, --I am submitting for fiscal 1963 a balanced Federal Budget. This is a joint responsibility, requiring Congressional cooperation on appropriations, and on three sources of income in particular: (1) First, an increase in postal rates, to end the postal deficit; (2) Secondly, passage of the tax reforms previously urged, to remove unwarranted tax preferences, and to apply to dividends and to interest the same withholding requirements we have long applied to wages; and (3) Third, extension of the present excise and corporation tax rates, except for those changes--which will be recommended in a message--affecting transportation. III. GETTING AMERICA MOVING But a stronger nation and economy require more than a balanced Budget. They require progress in those programs that spur our growth and fortify our strength. CITIES A strong America depends on its cities-America's glory, and sometimes America's shame. To substitute sunlight for congestion and progress for decay, we have stepped up existing urban renewal and housing programs, and launched new ones--redoubled the attack on water pollution--speeded aid to airports, hospitals, highways, and our declining mass transit systems--and secured new weapons to combat organized crime, racketeering, and youth delinquency, assisted by the coordinated and hard-hitting efforts of our investigative services: the FBI, the Internal Revenue, the Bureau of Narcotics, and many others. We shall need further anti-crime, mass transit, and transportation legislation--and new tools to fight air pollution. And with all this effort under way, both equity and commonsense require that our nation's urban areas--containing three-fourths of our population--sit as equals at the Cabinet table. I urge a new Department of Urban Affairs and Housing. AGRICULTURE AND RESOURCES A strong America also depends on its farms and natural resources. American farmers took heart in 1961--from a billion dollar rise in farm income--and from a hopeful start on reducing the farm surpluses. But we are still operating under a patchwork accumulation of old laws, which cost us $1 billion a year in CCC carrying charges alone, yet fail to halt rural poverty or boost farm earnings. Our task is to master and turn to fully fruitful ends the magnificent productivity of our farms and farmers. The revolution on our own countryside stands in the sharpest contrast to the repeated farm failures of the Communist nations and is a source of pride to us all. Since 1950 our agricultural output per man-hour has actually doubled! Without new, realistic measures, it will someday swamp our farmers and our taxpayers in a national scandal or a farm depression. I will, therefore, submit to the Congress a new comprehensive farm program--tailored to fit the use of our land and the supplies of each crop to the long-range needs of the sixties--and designed to prevent chaos in the sixties with a program of commonsense. We also need for the sixties--if we are to bequeath our full national estate to our heirs--a new long-range conservation and recreation program--expansion of our superb national parks and forests--preservation of our authentic wilderness areas-new starts on water and power projects as our population steadily increases--and expanded REA generation and transmission loans. CIVIL RIGHTS But America stands for progress in human rights as well as economic affairs, and a strong America requires the assurance of full and equal rights to all its citizens, of any race or of any color. This administration has shown as never before how much could be done through the full use of Executive powers--through the enforcement of laws already passed by the Congress-through persuasion, negotiation, and litigation, to secure the constitutional rights of all: the right to vote, the right to travel Without hindrance across State lines, and the right to free public education. I issued last March a comprehensive order to guarantee the right to equal employment opportunity in all Federal agencies and contractors. The Vice President's Committee thus created has done much, including the voluntary Plans for progress which, in all sections of the country, are achieving a quiet but striking success in opening up to all races new professional, supervisory, and other job opportunities. But there is much more to be done--by the Executive, by the courts, and by the Congress. Among the bills now pending before you, on which the executive departments will comment in detail, are appropriate methods of strengthening these basic rights which have our full support. The right to vote, for example, should no longer be denied through such arbitrary devices on a local level, sometimes abused, such as literacy tests and poll taxes. As we approach the 100th anniversary, next January, of the Emancipation Proclamation, let the acts of every branch of the Government--and every citizen--portray that righteousness does exalt a nation. HEALTH AND WELFARE"
	profileJson = getProfile(text)
	return profileJson

@app.route('/toneanalize')
def ToneAnalize(text=None):
	if text is None :
		text = "Mr. Vice President, my old colleague from Massachusetts and your new Speaker, John McCormack, Members of the 87th Congress, ladies and gentlemen: This week we begin anew our joint and separate efforts to build the American future. But, sadly, we build without a man who linked a long past with the present and looked strongly to the future. Mister Sam Rayburn is gone. Neither this House nor the Nation is the same without him. Members of the Congress, the Constitution makes us not rivals for power but partners for progress. We are all trustees for the American people, custodians of the American heritage. It is my task to report the State of the Union--to improve it is the task of us all. In the past year, I have traveled not only across our own land but to other lands-to the North and the South, and across the seas. And I have found--as I am sure you have, in your travels--that people everywhere, in spite of occasional disappointments, look to us--not to our wealth or power, but to the splendor of our ideals. For our Nation is commissioned by history to be either an observer of freedom's failure or the cause of its success. Our overriding obligation in the months ahead is to fulfill the world's hopes by fulfilling our own faith. 1. STRENGTHENING THE ECONOMY That task must begin at home. For if we cannot fulfill our own ideals here, we cannot expect others to accept them. And when the youngest child alive today has grown to the cares of manhood, our position in the world will be determined first of all by what provisions we make today--for his education, his health, and his opportunities for a good home and a good job and a good life. At home, we began the year in the valley of recession--we completed it on the high road of recovery and growth. With the help of new congressionally approved or administratively increased stimulants to our economy, the number of major surplus labor u areas has declined from 101 to 60; nonagricultural employment has increased by more than a million jobs; and the average factory work-week has risen to well over 40 hours. At year's end the economy which Mr. Khrushchev once called a stumbling horse was racing to new records in consumer spending, labor income, and industrial production. We are gratified--but we are not satisfied. Too many unemployed are still looking for the blessings of prosperity- As those who leave our schools and farms demand new jobs, automation takes old jobs away. To expand our growth and job opportunities, I urge on the Congress three measures:(1) First, the Manpower Training and Development Act, to stop the waste of able-bodied men and women who want to work, but whose only skill has been replaced by a machine, or moved with a mill, or shut down with a mine; (2) Second, the Youth Employment Opportunities Act, to help train and place not only the one million young Americans who are both out of school and out of work, but the twenty-six million young Americans entering the labor market in this decade; and (3) Third, the 8 percent tax credit for investment in machinery and equipment, which, combined with planned revisions of depreciation allowances, will spur our modernization, our growth, and our ability to compete abroad. Moreover--pleasant as it may be to bask in the warmth of recovery--let us not forget that we have suffered three recessions in the last 7 years. The time to repair the roof is when the sun is shining--by filling three basic gaps in our anti-recession protection. We need: (1) First, presidential standby authority, subject to congressional veto, to adjust personal income tax rates downward within a specified range and time, to slow down an economic decline before it has dragged us all down; (2) Second, presidential standby authority, upon a given rise in the rate of unemployment, to accelerate Federal and federally-aided capital improvement programs; and (3) Third, a permanent strengthening of our unemployment compensation system--to maintain for our fellow citizens searching for a job who cannot find it, their purchasing power and their living standards without constant resort--as we have seen in recent years by the Congress and the administrations-to temporary supplements. If we enact this six-part program, we can show the whole world that a free economy need not be an unstable economy--that a free system need not leave men unemployed--and that a free society is not only the most productive but the most stable form of organization yet fashioned by man. II. FIGHTING INFLATION But recession is only one enemy of a free economy--inflation is another. Last year, 1961, despite rising production and demand, consumer prices held almost steady--and wholesale prices declined. This is the best record of overall price stability of any comparable period of recovery since the end of World War II. Inflation too often follows in the shadow of growth--while price stability is made easy by stagnation or controls. But we mean to maintain both stability and growth in a climate of freedom. Our first line of defense against inflation is the good sense and public spirit of business and labor--keeping their total increases in wages and profits in step with productivity. There is no single statistical test to guide each company and each union. But I strongly urge them--for their country's interest, and for their own--to apply the test of the public interest to these transactions. Within this same framework of growth and wage-price stability: --This administration has helped keep our economy competitive by widening the access of small business to credit and Government contracts, and by stepping up the drive against monopoly, price-fixing, and racketeering; --We will submit a Federal Pay Reform bill aimed at giving our classified, postal, and other employees new pay scales more comparable to those of private industry; --We are holding the fiscal 1962 budget deficit far below the level incurred after the last recession in 1958; and, finally, --I am submitting for fiscal 1963 a balanced Federal Budget. This is a joint responsibility, requiring Congressional cooperation on appropriations, and on three sources of income in particular: (1) First, an increase in postal rates, to end the postal deficit; (2) Secondly, passage of the tax reforms previously urged, to remove unwarranted tax preferences, and to apply to dividends and to interest the same withholding requirements we have long applied to wages; and (3) Third, extension of the present excise and corporation tax rates, except for those changes--which will be recommended in a message--affecting transportation. III. GETTING AMERICA MOVING But a stronger nation and economy require more than a balanced Budget. They require progress in those programs that spur our growth and fortify our strength. CITIES A strong America depends on its cities-America's glory, and sometimes America's shame. To substitute sunlight for congestion and progress for decay, we have stepped up existing urban renewal and housing programs, and launched new ones--redoubled the attack on water pollution--speeded aid to airports, hospitals, highways, and our declining mass transit systems--and secured new weapons to combat organized crime, racketeering, and youth delinquency, assisted by the coordinated and hard-hitting efforts of our investigative services: the FBI, the Internal Revenue, the Bureau of Narcotics, and many others. We shall need further anti-crime, mass transit, and transportation legislation--and new tools to fight air pollution. And with all this effort under way, both equity and commonsense require that our nation's urban areas--containing three-fourths of our population--sit as equals at the Cabinet table. I urge a new Department of Urban Affairs and Housing. AGRICULTURE AND RESOURCES A strong America also depends on its farms and natural resources. American farmers took heart in 1961--from a billion dollar rise in farm income--and from a hopeful start on reducing the farm surpluses. But we are still operating under a patchwork accumulation of old laws, which cost us $1 billion a year in CCC carrying charges alone, yet fail to halt rural poverty or boost farm earnings. Our task is to master and turn to fully fruitful ends the magnificent productivity of our farms and farmers. The revolution on our own countryside stands in the sharpest contrast to the repeated farm failures of the Communist nations and is a source of pride to us all. Since 1950 our agricultural output per man-hour has actually doubled! Without new, realistic measures, it will someday swamp our farmers and our taxpayers in a national scandal or a farm depression. I will, therefore, submit to the Congress a new comprehensive farm program--tailored to fit the use of our land and the supplies of each crop to the long-range needs of the sixties--and designed to prevent chaos in the sixties with a program of commonsense. We also need for the sixties--if we are to bequeath our full national estate to our heirs--a new long-range conservation and recreation program--expansion of our superb national parks and forests--preservation of our authentic wilderness areas-new starts on water and power projects as our population steadily increases--and expanded REA generation and transmission loans. CIVIL RIGHTS But America stands for progress in human rights as well as economic affairs, and a strong America requires the assurance of full and equal rights to all its citizens, of any race or of any color. This administration has shown as never before how much could be done through the full use of Executive powers--through the enforcement of laws already passed by the Congress-through persuasion, negotiation, and litigation, to secure the constitutional rights of all: the right to vote, the right to travel Without hindrance across State lines, and the right to free public education. I issued last March a comprehensive order to guarantee the right to equal employment opportunity in all Federal agencies and contractors. The Vice President's Committee thus created has done much, including the voluntary Plans for progress which, in all sections of the country, are achieving a quiet but striking success in opening up to all races new professional, supervisory, and other job opportunities. But there is much more to be done--by the Executive, by the courts, and by the Congress. Among the bills now pending before you, on which the executive departments will comment in detail, are appropriate methods of strengthening these basic rights which have our full support. The right to vote, for example, should no longer be denied through such arbitrary devices on a local level, sometimes abused, such as literacy tests and poll taxes. As we approach the 100th anniversary, next January, of the Emancipation Proclamation, let the acts of every branch of the Government--and every citizen--portray that righteousness does exalt a nation. HEALTH AND WELFARE"
	profileJson = getToneAnalize(text)
	return profileJson

@app.route('/alchemylanguage')
def AlchemyLanguageV1(text=None):
	if text is None :
		text = "Mr. Vice President, my old colleague from Massachusetts and your new Speaker, John McCormack, Members of the 87th Congress, ladies and gentlemen: This week we begin anew our joint and separate efforts to build the American future. But, sadly, we build without a man who linked a long past with the present and looked strongly to the future. Mister Sam Rayburn is gone. Neither this House nor the Nation is the same without him. Members of the Congress, the Constitution makes us not rivals for power but partners for progress. We are all trustees for the American people, custodians of the American heritage. It is my task to report the State of the Union--to improve it is the task of us all. In the past year, I have traveled not only across our own land but to other lands-to the North and the South, and across the seas. And I have found--as I am sure you have, in your travels--that people everywhere, in spite of occasional disappointments, look to us--not to our wealth or power, but to the splendor of our ideals. For our Nation is commissioned by history to be either an observer of freedom's failure or the cause of its success. Our overriding obligation in the months ahead is to fulfill the world's hopes by fulfilling our own faith. 1. STRENGTHENING THE ECONOMY That task must begin at home. For if we cannot fulfill our own ideals here, we cannot expect others to accept them. And when the youngest child alive today has grown to the cares of manhood, our position in the world will be determined first of all by what provisions we make today--for his education, his health, and his opportunities for a good home and a good job and a good life. At home, we began the year in the valley of recession--we completed it on the high road of recovery and growth. With the help of new congressionally approved or administratively increased stimulants to our economy, the number of major surplus labor u areas has declined from 101 to 60; nonagricultural employment has increased by more than a million jobs; and the average factory work-week has risen to well over 40 hours. At year's end the economy which Mr. Khrushchev once called a stumbling horse was racing to new records in consumer spending, labor income, and industrial production. We are gratified--but we are not satisfied. Too many unemployed are still looking for the blessings of prosperity- As those who leave our schools and farms demand new jobs, automation takes old jobs away. To expand our growth and job opportunities, I urge on the Congress three measures:(1) First, the Manpower Training and Development Act, to stop the waste of able-bodied men and women who want to work, but whose only skill has been replaced by a machine, or moved with a mill, or shut down with a mine; (2) Second, the Youth Employment Opportunities Act, to help train and place not only the one million young Americans who are both out of school and out of work, but the twenty-six million young Americans entering the labor market in this decade; and (3) Third, the 8 percent tax credit for investment in machinery and equipment, which, combined with planned revisions of depreciation allowances, will spur our modernization, our growth, and our ability to compete abroad. Moreover--pleasant as it may be to bask in the warmth of recovery--let us not forget that we have suffered three recessions in the last 7 years. The time to repair the roof is when the sun is shining--by filling three basic gaps in our anti-recession protection. We need: (1) First, presidential standby authority, subject to congressional veto, to adjust personal income tax rates downward within a specified range and time, to slow down an economic decline before it has dragged us all down; (2) Second, presidential standby authority, upon a given rise in the rate of unemployment, to accelerate Federal and federally-aided capital improvement programs; and (3) Third, a permanent strengthening of our unemployment compensation system--to maintain for our fellow citizens searching for a job who cannot find it, their purchasing power and their living standards without constant resort--as we have seen in recent years by the Congress and the administrations-to temporary supplements. If we enact this six-part program, we can show the whole world that a free economy need not be an unstable economy--that a free system need not leave men unemployed--and that a free society is not only the most productive but the most stable form of organization yet fashioned by man. II. FIGHTING INFLATION But recession is only one enemy of a free economy--inflation is another. Last year, 1961, despite rising production and demand, consumer prices held almost steady--and wholesale prices declined. This is the best record of overall price stability of any comparable period of recovery since the end of World War II. Inflation too often follows in the shadow of growth--while price stability is made easy by stagnation or controls. But we mean to maintain both stability and growth in a climate of freedom. Our first line of defense against inflation is the good sense and public spirit of business and labor--keeping their total increases in wages and profits in step with productivity. There is no single statistical test to guide each company and each union. But I strongly urge them--for their country's interest, and for their own--to apply the test of the public interest to these transactions. Within this same framework of growth and wage-price stability: --This administration has helped keep our economy competitive by widening the access of small business to credit and Government contracts, and by stepping up the drive against monopoly, price-fixing, and racketeering; --We will submit a Federal Pay Reform bill aimed at giving our classified, postal, and other employees new pay scales more comparable to those of private industry; --We are holding the fiscal 1962 budget deficit far below the level incurred after the last recession in 1958; and, finally, --I am submitting for fiscal 1963 a balanced Federal Budget. This is a joint responsibility, requiring Congressional cooperation on appropriations, and on three sources of income in particular: (1) First, an increase in postal rates, to end the postal deficit; (2) Secondly, passage of the tax reforms previously urged, to remove unwarranted tax preferences, and to apply to dividends and to interest the same withholding requirements we have long applied to wages; and (3) Third, extension of the present excise and corporation tax rates, except for those changes--which will be recommended in a message--affecting transportation. III. GETTING AMERICA MOVING But a stronger nation and economy require more than a balanced Budget. They require progress in those programs that spur our growth and fortify our strength. CITIES A strong America depends on its cities-America's glory, and sometimes America's shame. To substitute sunlight for congestion and progress for decay, we have stepped up existing urban renewal and housing programs, and launched new ones--redoubled the attack on water pollution--speeded aid to airports, hospitals, highways, and our declining mass transit systems--and secured new weapons to combat organized crime, racketeering, and youth delinquency, assisted by the coordinated and hard-hitting efforts of our investigative services: the FBI, the Internal Revenue, the Bureau of Narcotics, and many others. We shall need further anti-crime, mass transit, and transportation legislation--and new tools to fight air pollution. And with all this effort under way, both equity and commonsense require that our nation's urban areas--containing three-fourths of our population--sit as equals at the Cabinet table. I urge a new Department of Urban Affairs and Housing. AGRICULTURE AND RESOURCES A strong America also depends on its farms and natural resources. American farmers took heart in 1961--from a billion dollar rise in farm income--and from a hopeful start on reducing the farm surpluses. But we are still operating under a patchwork accumulation of old laws, which cost us $1 billion a year in CCC carrying charges alone, yet fail to halt rural poverty or boost farm earnings. Our task is to master and turn to fully fruitful ends the magnificent productivity of our farms and farmers. The revolution on our own countryside stands in the sharpest contrast to the repeated farm failures of the Communist nations and is a source of pride to us all. Since 1950 our agricultural output per man-hour has actually doubled! Without new, realistic measures, it will someday swamp our farmers and our taxpayers in a national scandal or a farm depression. I will, therefore, submit to the Congress a new comprehensive farm program--tailored to fit the use of our land and the supplies of each crop to the long-range needs of the sixties--and designed to prevent chaos in the sixties with a program of commonsense. We also need for the sixties--if we are to bequeath our full national estate to our heirs--a new long-range conservation and recreation program--expansion of our superb national parks and forests--preservation of our authentic wilderness areas-new starts on water and power projects as our population steadily increases--and expanded REA generation and transmission loans. CIVIL RIGHTS But America stands for progress in human rights as well as economic affairs, and a strong America requires the assurance of full and equal rights to all its citizens, of any race or of any color. This administration has shown as never before how much could be done through the full use of Executive powers--through the enforcement of laws already passed by the Congress-through persuasion, negotiation, and litigation, to secure the constitutional rights of all: the right to vote, the right to travel Without hindrance across State lines, and the right to free public education. I issued last March a comprehensive order to guarantee the right to equal employment opportunity in all Federal agencies and contractors. The Vice President's Committee thus created has done much, including the voluntary Plans for progress which, in all sections of the country, are achieving a quiet but striking success in opening up to all races new professional, supervisory, and other job opportunities. But there is much more to be done--by the Executive, by the courts, and by the Congress. Among the bills now pending before you, on which the executive departments will comment in detail, are appropriate methods of strengthening these basic rights which have our full support. The right to vote, for example, should no longer be denied through such arbitrary devices on a local level, sometimes abused, such as literacy tests and poll taxes. As we approach the 100th anniversary, next January, of the Emancipation Proclamation, let the acts of every branch of the Government--and every citizen--portray that righteousness does exalt a nation. HEALTH AND WELFARE"
	profileJson = getAlchemyLanguageV1(text)
	return profileJson

if __name__ == '__main__':
    app.run()
